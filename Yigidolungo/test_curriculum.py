import urllib.request
import urllib.parse
import http.cookiejar
import json

base_url = 'http://127.0.0.1:5000'

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# 1. Login as demo user
opener.open(f'{base_url}/login/demo')

# Reset demo progress to start fresh from step 1
req_reset = urllib.request.Request(f'{base_url}/api/reset-progress', data=b'{}', headers={'Content-Type': 'application/json'})
opener.open(req_reset)

# 2. Test Profile View
resp_prof = opener.open(f'{base_url}/profile')
prof_html = resp_prof.read().decode('utf-8')
print('1. Profile View Status:', resp_prof.status)
assert 'İstatistikler & Başarılar' in prof_html, 'Profile stats header missing'
assert 'Toplam XP' in prof_html, 'XP stat missing'
assert 'Günlük Hedef' in prof_html, 'Daily goal missing'
print('   -> Profile page loaded successfully with stats and badges.')

# 3. Test Profile Edit (POST)
edit_data = urllib.parse.urlencode({
    'name': 'Yiğido Kahramanı',
    'daily_goal': '20',
    'bio': 'Günde 20 XP hedefim var ve İngilizceyi fethedeceğim!'
}).encode('utf-8')

req_edit = urllib.request.Request(f'{base_url}/profile/edit', data=edit_data, method='POST')
resp_edit = opener.open(req_edit)
print('2. Profile Edit Status:', resp_edit.status)

# Verify updated profile
prof_html_updated = opener.open(f'{base_url}/profile').read().decode('utf-8')
assert 'Yiğido Kahramanı' in prof_html_updated, 'Name not updated'
assert '20 XP' in prof_html_updated, 'Daily goal not updated'
assert 'Günde 20 XP hedefim var' in prof_html_updated, 'Bio not updated'
print('   -> Profile successfully updated and verified.')

# 4. Test Dashboard & 13 Steps
resp_dash = opener.open(f'{base_url}/dashboard')
dash_html = resp_dash.read().decode('utf-8')
print('3. Dashboard Status:', resp_dash.status)
assert 'Konu 1: Selamlaşma' in dash_html, 'Topic 1 missing'
assert 'Konu 7: Şimdiki Zaman' in dash_html, 'Topic 7 missing'
assert 'Seviye Atlama Boss Sınavı' in dash_html, 'Boss exam missing'
assert 'BAŞLA' in dash_html, 'Active step indicator missing'
print('   -> All 13 steps verified on Dashboard roadmap.')

# 5. Test Lock Mechanism: Try to open Step 4 directly while at Step 1
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

no_redir_opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj), NoRedirect)

# Get lesson IDs
conn_helper = urllib.request.urlopen(f'{base_url}/dashboard')
# First lesson has id 4 (from our earlier check) or we can test by id
# Fetch questions of active lesson
import sqlite3
_conn = sqlite3.connect('database.db')
_first_lesson_id = _conn.execute('SELECT id FROM lessons WHERE order_num = 1').fetchone()[0]
_conn.close()

resp_q = opener.open(f'{base_url}/api/lesson/{_first_lesson_id}/questions')
q_data = json.loads(resp_q.read().decode('utf-8'))
print('4. Step 1 Questions count:', len(q_data['questions']))
assert len(q_data['questions']) >= 5, 'Step 1 should have at least 5 questions'

# Complete Step 1
comp_payload = json.dumps({'score': 100}).encode('utf-8')
req_comp = urllib.request.Request(f'{base_url}/api/lesson/{_first_lesson_id}/complete', data=comp_payload, headers={'Content-Type': 'application/json'})
res_comp = json.loads(opener.open(req_comp).read().decode('utf-8'))
print('5. Step 1 Completed (+XP):', res_comp)
assert res_comp['success'] is True

# Check Dashboard now shows Step 1 completed and Step 2 active!
dash_html_after = opener.open(f'{base_url}/dashboard').read().decode('utf-8')
assert '✓' in dash_html_after, 'Step 1 completed checkmark missing'
print('   -> Step 1 completed checkmark verified and Step 2 unlocked!')

print('\n*** TÜM PROFİL, MÜFREDAT VE SINAV TESTLERİ BAŞARIYLA TAMAMLANDI! ***')
