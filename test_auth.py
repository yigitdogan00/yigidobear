import urllib.request
import urllib.parse
import http.cookiejar
import json

base_url = 'http://127.0.0.1:5000'

# Create a cookie opener to maintain session across requests
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# 1. Test unauthenticated redirect
class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

no_redir_opener = urllib.request.build_opener(NoRedirectHandler)

try:
    resp = no_redir_opener.open(f'{base_url}/dashboard')
    print('Unexpected 200 on /dashboard without session')
except urllib.error.HTTPError as e:
    print('1. Logged out user redirect test (HTTP status):', e.code)
    assert e.code in (302, 303), f'Expected redirect 302, got {e.code}'
    assert '/login' in e.headers.get('Location', ''), 'Did not redirect to /login'
    print('   -> Successfully redirected to /login')

# 2. Test Login Page loads
resp_login = opener.open(f'{base_url}/login')
login_html = resp_login.read().decode('utf-8')
print('2. Login page status:', resp_login.status)
assert 'Google ile Devam Et' in login_html, 'Google login button not found'
assert 'YiğidoBear' in login_html, 'Brand not found on login page'
print('   -> Login page loaded with Google OAuth button and mascot!')

# 3. Test Demo / Guest Login
resp_demo = opener.open(f'{base_url}/login/demo')
print('3. Demo login status after redirect:', resp_demo.status)
dashboard_html = resp_demo.read().decode('utf-8')
assert 'Çıkış' in dashboard_html, 'Logout button missing in dashboard navbar'
assert 'Ünite 1' in dashboard_html, 'Unit 1 missing in dashboard'
print('   -> Successfully logged in via demo, dashboard opened with user profile & logout button!')

# 4. Test Check Answer with session
import sqlite3
_conn = sqlite3.connect('database.db')
_q = _conn.execute('SELECT id, correct_answer FROM questions ORDER BY id ASC LIMIT 1').fetchone()
_conn.close()

payload_correct = json.dumps({'question_id': _q[0], 'answer': _q[1]}).encode('utf-8')
req_ans = urllib.request.Request(f'{base_url}/api/check-answer', data=payload_correct, headers={'Content-Type': 'application/json'})
res_correct = json.loads(opener.open(req_ans).read().decode('utf-8'))
print('4. Authenticated Answer check:', res_correct)
assert res_correct['is_correct'] is True

# 5. Test Logout
resp_logout = opener.open(f'{base_url}/logout')
print('5. Logout status:', resp_logout.status)
after_logout_html = resp_logout.read().decode('utf-8')
assert 'Misafir Öğrenci' in after_logout_html, 'Did not land back on guest dashboard after logout'

resp_login = opener.open(f'{base_url}/login')
login_page_html = resp_login.read().decode('utf-8')
assert 'Google ile Devam Et' in login_page_html, 'Login page missing Google continue button'
print('   -> Successfully logged out and verified guest dashboard & login page!')

print('\n*** TÜM GOOGLE OAUTH VE AUTH TESTLERİ EKSİKSİZ BAŞARILI! ***')
