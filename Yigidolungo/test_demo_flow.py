import urllib.request
import json
import http.cookiejar
import sqlite3

base_url = 'http://127.0.0.1:5000'

conn = sqlite3.connect('database.db')
first_lesson_id = conn.execute('SELECT id FROM lessons WHERE order_num = 1').fetchone()[0]
second_lesson_id = conn.execute('SELECT id FROM lessons WHERE order_num = 2').fetchone()[0]
conn.close()

# 1. Fresh Visitor landing on '/' in clean session (like Incognito)
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

resp = opener.open(f'{base_url}/')
assert resp.status == 200, f'Expected 200 on landing, got {resp.status}'
landing_html = resp.read().decode('utf-8')

# Verify Guest account initialized and landed on dashboard directly
assert 'Misafir Öğrenci' in landing_html, 'Guest user name missing on dashboard'
assert 'Ünite 1' in landing_html, 'Unit 1 missing on dashboard'
assert 'BAŞLA' in landing_html, 'Active step indicator missing for Topic 1'
print('1. Incognito/Fresh visitor lands directly on Dashboard with Misafir account (Topic 1 selectable: BAŞLA).')

# 2. Select and open Unit 1 - Topic 1
resp_lesson = opener.open(f'{base_url}/lesson/{first_lesson_id}')
assert resp_lesson.status == 200
lesson_html = resp_lesson.read().decode('utf-8')

assert 'isDemo = true' in lesson_html, 'isDemo flag should be true for guest user'
assert 'demo-conversion-modal' in lesson_html, 'Demo conversion modal missing'
assert 'Harika Gidiyorsun!' in lesson_html, 'Modal title missing'
assert 'Google ile Giriş Yap' in lesson_html, 'Google login button missing in modal'
print('2. Topic 1 selected & opened: isDemo=true verified, 3rd question conversion modal present.')

# 3. Guest trying to open Step 2 without authentication
resp_step2 = opener.open(f'{base_url}/lesson/{second_lesson_id}')
assert 'locked=' in resp_step2.url or '/dashboard' in resp_step2.url, 'Guest must not be allowed to open Step 2'
print('3. Guest attempt to open Step 2 strictly blocked.')

# 4. Authenticated user flow (Full access)
opener.open(f'{base_url}/login/demo')
resp_auth_lesson = opener.open(f'{base_url}/lesson/{first_lesson_id}')
auth_html = resp_auth_lesson.read().decode('utf-8')
assert 'isDemo = false' in auth_html, 'isDemo should be false for authenticated user'
print('4. Authenticated user on lesson: isDemo=false verified (all 10 questions unlocked).')

print('\n*** TÜM MİSAFİR HESAP VE DEMO DÖNÜŞÜM TESTLERİ BAŞARIYLA GEÇTİ! ***')
