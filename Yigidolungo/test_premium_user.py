import urllib.request
import json
import http.cookiejar
import sqlite3

base_url = 'http://127.0.0.1:5000'
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# 1. Login as demo user (which logs in as Yiğit DOĞAN since google_id is present)
opener.open(f'{base_url}/login/demo')

print("--- 1. Testing Premium Status for Yiğit DOĞAN ---")
conn = sqlite3.connect('database.db')
conn.row_factory = sqlite3.Row
user = conn.execute("SELECT * FROM users WHERE name LIKE '%Yiğit%' OR email = 'yigitdogan5134@gmail.com'").fetchone()
conn.close()

assert user is not None, "Yiğit DOĞAN not found in database!"
print(f"   -> User: {user['name']} ({user['email']}), is_premium: {user['is_premium']}")
assert user['is_premium'] == 1, "Yiğit DOĞAN is_premium should be 1!"

print("\n--- 2. Testing Dashboard & Profile VIP Indicators ---")
dash_html = opener.open(f'{base_url}/dashboard').read().decode('utf-8')
assert '∞ PLUS' in dash_html, "Header should display ∞ PLUS for premium user"
assert 'Sınırsız Can (Plus Aktif)' in dash_html, "Dashboard should display Sınırsız Can (Plus Aktif)"
assert '👑' in dash_html, "Crown badge should be present"
print("   -> Dashboard VIP view verified!")

prof_html = opener.open(f'{base_url}/profile').read().decode('utf-8')
assert 'YiğidoBear PLUS' in prof_html, "Profile should display YiğidoBear PLUS badge"
assert '∞ (Sınırsız)' in prof_html, "Profile should display ∞ (Sınırsız) hearts"
print("   -> Profile VIP view verified!")

print("\n--- 3. Testing /api/heart-status for Premium User ---")
status_res = json.loads(opener.open(f'{base_url}/api/heart-status').read().decode('utf-8'))
print("   -> /api/heart-status response:", status_res)
assert status_res['is_premium'] is True, "is_premium must be True"
assert status_res['hearts'] == 5, "hearts must be 5"
assert status_res['is_full'] is True, "is_full must be True"
assert status_res['remaining_seconds'] == 0, "remaining_seconds must be 0"

print("\n--- 4. Testing Infinite Hearts on Wrong Answer ---")
conn = sqlite3.connect('database.db')
q_id = conn.execute('SELECT id FROM questions LIMIT 1').fetchone()[0]
conn.close()

wrong_payload = json.dumps({'question_id': q_id, 'answer': 'Tamamen Yanlış Şık'}).encode('utf-8')
req_wrong = urllib.request.Request(f'{base_url}/api/check-answer', data=wrong_payload, headers={'Content-Type': 'application/json'})
res_wrong = json.loads(opener.open(req_wrong).read().decode('utf-8'))

print("   -> Wrong answer response for Premium user:", res_wrong)
assert res_wrong['is_correct'] is False, "Answer should be incorrect"
assert res_wrong['hearts'] == 5, f"Premium user should NOT lose hearts! Got {res_wrong['hearts']}"
assert res_wrong['is_hearts_full'] is True, "Premium user hearts should remain full"

conn = sqlite3.connect('database.db')
db_user = conn.execute('SELECT hearts, last_heart_loss_time FROM users WHERE id = ?', (user['id'],)).fetchone()
conn.close()
print(f"   -> DB after wrong answer: hearts={db_user[0]}, last_heart_loss_time={db_user[1]}")
assert db_user[0] == 5, "DB hearts should remain 5"
assert db_user[1] is None, "last_heart_loss_time should remain None"

print("\n*** YİĞİT DOĞAN PREMİUM / PLUS HESAP DOĞRULAMASI %100 BAŞARIYLA GEÇTİ! ***")
