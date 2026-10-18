import urllib.request
import json
import http.cookiejar
import sqlite3
import datetime

base_url = 'http://127.0.0.1:5000'
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# 1. Login demo as standard user
opener.open(f'{base_url}/login/demo?user=standard')

# Reset progress and ensure 5 hearts
req_refill = urllib.request.Request(f'{base_url}/api/refill-hearts', data=b'{}', headers={'Content-Type': 'application/json'})
opener.open(req_refill)

print("--- 1. Testing UI Button Removal & Full Hearts Status ---")
dash_html = opener.open(f'{base_url}/dashboard').read().decode('utf-8')
assert 'Canları Yenile (5/5)' not in dash_html, "CANLARI YENİLE (5/5) button should be removed from dashboard!"
assert 'Canlar Dolu' in dash_html, "Canlar Dolu should be visible when hearts are 5"
assert 'SINIRSIZ CAN (PLUS)' in dash_html, "SINIRSIZ CAN (PLUS) button should be visible"
assert 'YiğidoBear Plus ile Asla Durma!' in dash_html, "Plus promo modal title missing"
assert 'Sonsuz Can' in dash_html, "Plus feature Sonsuz Can missing"
assert 'Reklamsız Ders' in dash_html, "Plus feature Reklamsız Ders missing"
assert 'Özel Hata Pratikleri' in dash_html, "Plus feature Özel Hata Pratikleri missing"
assert "Plus'ı Keşfet" in dash_html, "Plus'ı Keşfet button missing"
print("   -> UI verified: old refill button removed, timer banner present, Plus button and modal ready.")

print("\n--- 2. Testing Heart Loss & 15-Minute Countdown Start ---")
# Call check-answer with wrong answer
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('SELECT id FROM questions LIMIT 1')
q_id = cursor.fetchone()[0]
conn.close()

wrong_payload = json.dumps({'question_id': q_id, 'answer': 'Wrong Answer XYZ'}).encode('utf-8')
req_wrong = urllib.request.Request(f'{base_url}/api/check-answer', data=wrong_payload, headers={'Content-Type': 'application/json'})
res_wrong = json.loads(opener.open(req_wrong).read().decode('utf-8'))

print("   -> Wrong answer response:", res_wrong)
assert res_wrong['hearts'] == 4, f"Expected 4 hearts, got {res_wrong['hearts']}"
assert res_wrong['is_hearts_full'] is False, "is_hearts_full should be False"
assert 0 < res_wrong['remaining_seconds'] <= 900, f"Remaining seconds {res_wrong['remaining_seconds']} out of range"

# Verify DB timestamp recorded
conn = sqlite3.connect('database.db')
demo_id = conn.execute("SELECT id FROM users WHERE google_id IS NOT NULL AND (is_premium = 0 OR is_premium IS NULL) LIMIT 1").fetchone()[0]
user_row = conn.execute('SELECT hearts, last_heart_loss_time FROM users WHERE id = ?', (demo_id,)).fetchone()
conn.close()
print(f"   -> DB State after heart loss: hearts={user_row[0]}, last_heart_loss_time={user_row[1]}")
assert user_row[0] == 4
assert user_row[1] is not None, "last_heart_loss_time should be recorded!"

# Verify /api/heart-status endpoint
status_res = json.loads(opener.open(f'{base_url}/api/heart-status').read().decode('utf-8'))
print("   -> /api/heart-status:", status_res)
assert status_res['hearts'] == 4
assert status_res['is_full'] is False
assert 0 < status_res['remaining_seconds'] <= 900

print("\n--- 3. Testing 15-Minute Regeneration Simulation ---")
# Simulate 16 minutes having elapsed (960 seconds ago)
sixteen_mins_ago = (datetime.datetime.now() - datetime.timedelta(minutes=16)).isoformat()
conn = sqlite3.connect('database.db')
conn.execute('UPDATE users SET last_heart_loss_time = ? WHERE id = ?', (sixteen_mins_ago, demo_id))
conn.commit()
conn.close()

# Calling /api/heart-status should automatically trigger sync and recover 1 heart back to 5!
status_regen = json.loads(opener.open(f'{base_url}/api/heart-status').read().decode('utf-8'))
print("   -> Status after 16 minutes elapsed:", status_regen)
assert status_regen['hearts'] == 5, f"Expected regenerated hearts 5, got {status_regen['hearts']}"
assert status_regen['is_full'] is True, "is_full should be True when 5 hearts"
assert status_regen['remaining_seconds'] == 0, "remaining_seconds should be 0"

# Verify in DB
conn = sqlite3.connect('database.db')
user_final = conn.execute('SELECT hearts, last_heart_loss_time FROM users WHERE id = ?', (demo_id,)).fetchone()
conn.close()
print(f"   -> DB State after regeneration: hearts={user_final[0]}, last_heart_loss_time={user_final[1]}")
assert user_final[0] == 5
assert user_final[1] is None, "last_heart_loss_time should be cleared to NULL when full"

print("\n--- 4. Testing Multi-Heart Regeneration (e.g. 3 hearts, 16 mins elapsed -> 4 hearts, 14 mins left) ---")
conn = sqlite3.connect('database.db')
conn.execute('UPDATE users SET hearts = 3, last_heart_loss_time = ? WHERE id = ?', (sixteen_mins_ago, demo_id))
conn.commit()
conn.close()

status_multi = json.loads(opener.open(f'{base_url}/api/heart-status').read().decode('utf-8'))
print("   -> Status multi-heart regeneration:", status_multi)
assert status_multi['hearts'] == 4, f"Expected 4 hearts, got {status_multi['hearts']}"
assert status_multi['is_full'] is False, "Should still be recharging"
# Since 16 mins passed, 15 was consumed for heart 3->4, and 1 min passed toward heart 4->5, so ~14 mins left (800-860s)
assert 800 <= status_multi['remaining_seconds'] <= 860, f"Remaining seconds unexpected: {status_multi['remaining_seconds']}"

# Refill for clean state
opener.open(req_refill)
print("\n*** TÜM CAN MEKANİZMASI, 15 DAKİKALIK GERİ SAYIM VE PLUS MONETIZATION TESTLERİ BAŞARIYLA GEÇTİ! ***")
