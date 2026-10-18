import urllib.request
import json
import http.cookiejar
import sqlite3

base_url = 'http://127.0.0.1:5000'
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

print("=== 1. Testing Database 'units' Schema and Definitions ===")
conn = sqlite3.connect('database.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Check table info
cursor.execute("PRAGMA table_info(units)")
unit_cols = [c[1] for c in cursor.fetchall()]
print("   -> Units columns:", unit_cols)
assert 'order_index' in unit_cols, "order_index missing in units table!"
assert 'is_unlocked' in unit_cols, "is_unlocked missing in units table!"

# Check 4 units
units = conn.execute("SELECT id, order_index, is_unlocked, title FROM units ORDER BY order_index ASC").fetchall()
print(f"   -> Found {len(units)} units:")
for u in units:
    print(f"      [{u['order_index']}] {u['title']} - Unlocked: {bool(u['is_unlocked'])}")

assert len(units) >= 4, f"Expected at least 4 units, found {len(units)}"
assert units[0]['is_unlocked'] == 1, "Unit 1 must be unlocked!"
assert units[1]['is_unlocked'] == 0, "Unit 2 must be locked initially!"
assert units[2]['is_unlocked'] == 0, "Unit 3 must be locked initially!"
assert units[3]['is_unlocked'] == 0, "Unit 4 must be locked initially!"
conn.close()

print("\n=== 2. Testing Dashboard Visual & S-Curve Elements ===")
# Login demo (Yiğit DOĞAN)
opener.open(f'{base_url}/login/demo')
dash_html = opener.open(f'{base_url}/dashboard').read().decode('utf-8')

# S-Curve snake winding
assert 'step-snake-left' in dash_html, "S-Curve step-snake-left missing!"
assert 'step-snake-right' in dash_html, "S-Curve step-snake-right missing!"

# Bouncing Mascot Guide on active step
assert 'active-mascot-guide' in dash_html, "Bouncing Mascot Guide on active step missing!"
assert 'mascot-bouncing-icon' in dash_html, "mascot-bouncing-icon missing!"

# Glassmorphism and Unit Banner
assert 'unit-banner' in dash_html, "unit-banner missing!"
assert 'unit-guide-btn' in dash_html, "unit-guide-btn glassmorphism button missing!"
assert '📖 Kılavuz' in dash_html, "Kılavuz button missing!"
assert '👤 Profil' in dash_html, "Profil access missing!"

# Sections & Units Navigation Card
assert 'units-nav-card' in dash_html, "units-nav-card missing in sidebar!"
assert 'Bölümler & Üniteler' in dash_html, "Bölümler & Üniteler card title missing!"
assert 'Şu Anki Konum' in dash_html, "Şu Anki Konum badge missing!"
assert 'showUnitLockedToast' in dash_html, "showUnitLockedToast handler missing!"

# Simplified Premium Hearts Card
assert 'Sınırsız Can (Plus Aktif)' in dash_html, "Simplified Sınırsız Can (Plus Aktif) badge missing!"

# Guidebook Modal & Dev Reset Button
assert 'unit-guide-modal' in dash_html, "unit-guide-modal missing!"
assert 'Temel İletişim Rehberi' in dash_html, "Temel İletişim Rehberi title missing!"
assert 'dev-reset-btn' in dash_html, "dev-reset-btn missing!"
assert 'reset-progress' in dash_html, "reset-progress route missing!"

print("   -> All visual elements, S-Curve, Bouncing Mascot, Guidebook modal, and Navigation card verified!")

print("\n=== 3. Testing Route Protection for Locked Unit ===")
# Custom redirect handler to intercept redirect
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

no_redir_opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj), NoRedirect)

conn = sqlite3.connect('database.db')
u2_id = conn.execute("SELECT id FROM units WHERE order_index = 2 OR order_num = 2").fetchone()[0]
conn.close()

try:
    resp_locked = no_redir_opener.open(f'{base_url}/unit/{u2_id}')
    status_code = resp_locked.status
    location = resp_locked.headers.get('Location', '')
except urllib.error.HTTPError as e:
    status_code = e.code
    location = e.headers.get('Location', '')

print(f"   -> Direct GET /unit/{u2_id}: Status {status_code}, Redirect Location: {location}")
assert status_code in (301, 302, 303, 307), f"Expected redirect, got {status_code}"
assert 'locked=unit_locked' in location, "Should redirect to dashboard with locked=unit_locked!"

# Verify redirected dashboard shows locked alert
full_redir_url = location if location.startswith('http') else f'{base_url}{location}'
redir_dash = opener.open(full_redir_url).read().decode('utf-8')
assert 'Kilitli Ünite Uyarısı' in redir_dash, "Kilitli Ünite Uyarısı alert should be rendered!"
print("   -> Route protection verified: User prevented from entering locked Unit 2.")

print("\n=== 4. Testing Unit 2 Auto-Unlock upon Completing Boss Exam ===")
conn = sqlite3.connect('database.db')
conn.row_factory = sqlite3.Row
boss_lesson = conn.execute("SELECT id, order_num, is_exam, title FROM lessons WHERE order_num = 13 OR title LIKE '%Boss%'").fetchone()
conn.close()
safe_title = boss_lesson['title'].encode('ascii', 'ignore').decode('ascii')
print(f"   -> Boss Lesson: ID {boss_lesson['id']} - {safe_title}")

# Complete Boss Exam
comp_payload = json.dumps({'score': 100}).encode('utf-8')
req_comp = urllib.request.Request(f'{base_url}/api/lesson/{boss_lesson["id"]}/complete', data=comp_payload, headers={'Content-Type': 'application/json'})
res_comp = json.loads(opener.open(req_comp).read().decode('utf-8'))
print("   -> Complete Boss Exam API response:", res_comp)
assert res_comp['success'] is True, "Lesson complete API failed"

# Check DB: Unit 2 should now be unlocked (is_unlocked = 1)!
conn = sqlite3.connect('database.db')
u2_unlocked = conn.execute("SELECT is_unlocked FROM units WHERE id = ?", (u2_id,)).fetchone()[0]
conn.close()
print(f"   -> DB Unit 2 status after Boss Exam: is_unlocked = {u2_unlocked}")
assert u2_unlocked == 1, "Unit 2 should be automatically unlocked after completing Unit 1 Boss Exam!"

# Test visiting /unit/{u2_id} now succeeds without locked redirect!
try:
    resp_unlocked = no_redir_opener.open(f'{base_url}/unit/{u2_id}')
    status_code_unlocked = resp_unlocked.status
    location_unlocked = resp_unlocked.headers.get('Location', '')
except urllib.error.HTTPError as e:
    status_code_unlocked = e.code
    location_unlocked = e.headers.get('Location', '')

print(f"   -> GET /unit/{u2_id} after unlock: Status {status_code_unlocked}, Location: {location_unlocked}")
assert 'locked=unit_locked' not in location_unlocked, "Should no longer be locked!"

# Reset progress for clean test state
opener.open(urllib.request.Request(f'{base_url}/api/reset-progress', data=b'{}', headers={'Content-Type': 'application/json'}))
conn = sqlite3.connect('database.db')
conn.execute("UPDATE units SET is_unlocked = 0 WHERE order_index >= 2")
conn.commit()
conn.close()

print("\n*** DASHBOARD S-CURVE, BÖLÜMLER KARTI, 4 ÜNİTE VE KİLİT MEKANİZMASI %100 BAŞARIYLA GEÇTİ! ***")
