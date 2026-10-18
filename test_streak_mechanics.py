import urllib.request
import json
import sqlite3
import datetime
import http.cookiejar

base_url = 'http://127.0.0.1:5000'

print('=== 1. Testing Database Schema for streak_count and last_study_date ===')
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('PRAGMA table_info(users)')
cols = [c[1] for c in cursor.fetchall()]
assert 'streak_count' in cols, "Missing 'streak_count' column in users table"
assert 'last_study_date' in cols, "Missing 'last_study_date' column in users table"
print('   -> users schema verified: streak_count and last_study_date exist.')

# Get test user ID
cursor.execute("SELECT id FROM users WHERE google_id = 'google-student-12345'")
row = cursor.fetchone()
if not row:
    cursor.execute("SELECT id FROM users WHERE google_id IS NOT NULL AND (is_premium = 0 OR is_premium IS NULL)")
    row = cursor.fetchone()
test_user_id = row[0]

# Get first lesson ID
cursor.execute("SELECT id FROM lessons WHERE order_num = 1")
lesson1_id = cursor.fetchone()[0]
conn.close()

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
opener.open(f'{base_url}/login/demo?user=standard')

today_dt = datetime.date.today()
today_str = today_dt.strftime('%Y-%m-%d')
yesterday_str = (today_dt - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
three_days_ago_str = (today_dt - datetime.timedelta(days=3)).strftime('%Y-%m-%d')

print('\n=== 2. Testing Scenario A: Fresh/Empty Study Date (Streak = 1) ===')
conn = sqlite3.connect('database.db')
conn.execute("UPDATE users SET streak_count = 0, streak = 0, last_study_date = NULL WHERE id = ?", (test_user_id,))
conn.commit()
conn.close()

# Verify pre-lesson dashboard has streak-inactive
resp_pre = opener.open(f'{base_url}/dashboard')
html_pre = resp_pre.read().decode('utf-8')
assert 'streak-inactive' in html_pre, 'Dashboard flame should be inactive before studying today'
print('   -> Verified dashboard has streak-inactive (dimmed flame) before completing a lesson today.')

# Complete lesson 1
req = urllib.request.Request(
    f'{base_url}/api/lesson/{lesson1_id}/complete',
    data=json.dumps({'score': 100}).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
res = json.loads(opener.open(req).read().decode('utf-8'))
assert res['success'] is True
assert res['streak_count'] == 1, f"Expected streak_count 1, got {res['streak_count']}"
assert res['last_study_date'] == today_str

# Check DB
conn = sqlite3.connect('database.db')
u = conn.execute("SELECT streak_count, streak, last_study_date FROM users WHERE id = ?", (test_user_id,)).fetchone()
conn.close()
assert u[0] == 1 and u[1] == 1 and u[2] == today_str
print(f'   -> Scenario A passed: streak_count=1, last_study_date={today_str}')

# Verify post-lesson dashboard has streak-active
resp_post = opener.open(f'{base_url}/dashboard')
html_post = resp_post.read().decode('utf-8')
assert 'streak-active' in html_post, 'Dashboard flame should be active after studying today'
print('   -> Verified dashboard has streak-active (flaming orange flame) after completing a lesson today.')

print('\n=== 3. Testing Scenario B: Same-Day 2nd Lesson (Streak remains unchanged) ===')
req2 = urllib.request.Request(
    f'{base_url}/api/complete-lesson',
    data=json.dumps({'lesson_id': lesson1_id}).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
res2 = json.loads(opener.open(req2).read().decode('utf-8'))
assert res2['success'] is True
assert res2['streak_count'] == 1, f"Expected streak_count to remain 1, got {res2['streak_count']}"
print('   -> Scenario B passed: Same-day second lesson kept streak_count at 1.')

print('\n=== 4. Testing Scenario C: Consecutive Day / Studied Yesterday (Streak increments by 1) ===')
conn = sqlite3.connect('database.db')
conn.execute("UPDATE users SET streak_count = 4, streak = 4, last_study_date = ? WHERE id = ?", (yesterday_str, test_user_id))
conn.commit()
conn.close()

res3 = json.loads(opener.open(req).read().decode('utf-8'))
assert res3['success'] is True
assert res3['streak_count'] == 5, f"Expected streak_count 5, got {res3['streak_count']}"
assert res3['last_study_date'] == today_str

conn = sqlite3.connect('database.db')
u3 = conn.execute("SELECT streak_count, streak, last_study_date FROM users WHERE id = ?", (test_user_id,)).fetchone()
conn.close()
assert u3[0] == 5 and u3[2] == today_str
print(f'   -> Scenario C passed: 4-day streak incremented to 5 on consecutive day study.')

print('\n=== 5. Testing Scenario D: Gap of Multiple Days / Missed Day (Streak resets to 1) ===')
conn = sqlite3.connect('database.db')
conn.execute("UPDATE users SET streak_count = 10, streak = 10, last_study_date = ? WHERE id = ?", (three_days_ago_str, test_user_id))
conn.commit()
conn.close()

res4 = json.loads(opener.open(req).read().decode('utf-8'))
assert res4['success'] is True
assert res4['streak_count'] == 1, f"Expected streak_count reset to 1, got {res4['streak_count']}"
assert res4['last_study_date'] == today_str

conn = sqlite3.connect('database.db')
u4 = conn.execute("SELECT streak_count, streak, last_study_date FROM users WHERE id = ?", (test_user_id,)).fetchone()
conn.close()
assert u4[0] == 1 and u4[2] == today_str
print(f'   -> Scenario D passed: 10-day streak with 3-day gap cleanly reset to 1 on new study.')

print('\n*** GÜNLÜK SERİ (STREAK / ATEŞ) MEKANİZMASI %100 BAŞARIYLA GEÇTİ! ***')
