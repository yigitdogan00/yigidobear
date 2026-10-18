import urllib.request
import json
import http.cookiejar

base_url = 'http://127.0.0.1:5000'

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# Authenticate first as standard user
opener.open(f'{base_url}/login/demo?user=standard')

# Refill hearts to start fresh with 5
req_refill = urllib.request.Request(f'{base_url}/api/refill-hearts', data=b'{}', headers={'Content-Type': 'application/json'})
opener.open(req_refill)

# 1. Dashboard
req = opener.open(f'{base_url}/dashboard')
html = req.read().decode('utf-8')
print('1. Dashboard Status:', req.status, 'HTML length:', len(html))
assert 'YiğidoBear' in html, 'YiğidoBear brand missing'
assert 'Ünite 1' in html, 'Unit 1 missing'

# 2. Lesson Questions
import sqlite3
conn = sqlite3.connect('database.db')
first_lesson_id = conn.execute('SELECT id FROM lessons ORDER BY order_num ASC LIMIT 1').fetchone()[0]

req_q = opener.open(f'{base_url}/api/lesson/{first_lesson_id}/questions')
q_data = json.loads(req_q.read().decode('utf-8'))
print('2. Questions Count:', len(q_data['questions']))
assert len(q_data['questions']) >= 4, 'Expected at least 4 questions'

for q in q_data['questions']:
    print(f"   - Soru {q['id']} ({q['type']})")

# 3. Check Correct Answer
q1 = q_data['questions'][0]
q1_corr = conn.execute('SELECT correct_answer FROM questions WHERE id = ?', (q1['id'],)).fetchone()[0]

payload_correct = json.dumps({'question_id': q1['id'], 'answer': q1_corr}).encode('utf-8')
req_ans = urllib.request.Request(f'{base_url}/api/check-answer', data=payload_correct, headers={'Content-Type': 'application/json'})
res_correct = json.loads(opener.open(req_ans).read().decode('utf-8'))
print('3. Doğru Cevap Testi:', res_correct)
assert res_correct['is_correct'] is True

# 4. Check Incorrect Answer (Can düşme testi)
payload_wrong = json.dumps({'question_id': q1['id'], 'answer': 'Tamamen Yanlış Şık XYZ'}).encode('utf-8')
req_wrong = urllib.request.Request(f'{base_url}/api/check-answer', data=payload_wrong, headers={'Content-Type': 'application/json'})
res_wrong = json.loads(opener.open(req_wrong).read().decode('utf-8'))
print('4. Yanlış Cevap Testi (Can Düşme):', res_wrong)
assert res_wrong['is_correct'] is False
assert res_wrong['hearts'] == 4

# 5. Check Word Order Answer
q2 = q_data['questions'][1]
q2_corr = conn.execute('SELECT correct_answer FROM questions WHERE id = ?', (q2['id'],)).fetchone()[0]
conn.close()

try:
    ans_list = json.loads(q2_corr)
except Exception:
    ans_list = q2_corr.split()

payload_word = json.dumps({'question_id': q2['id'], 'answer': ans_list}).encode('utf-8')
req_word = urllib.request.Request(f'{base_url}/api/check-answer', data=payload_word, headers={'Content-Type': 'application/json'})
res_word = json.loads(opener.open(req_word).read().decode('utf-8'))
print('5. Kelime Sıralama Testi:', res_word)
assert res_word['is_correct'] is True

# 6. Check Lesson Complete
payload_comp = json.dumps({'score': 100}).encode('utf-8')
req_comp = urllib.request.Request(f'{base_url}/api/lesson/{first_lesson_id}/complete', data=payload_comp, headers={'Content-Type': 'application/json'})
res_comp = json.loads(opener.open(req_comp).read().decode('utf-8'))
print('6. Ders Tamamlama Testi (+XP):', res_comp)
assert res_comp['success'] is True

# 7. Check Refill Hearts
req_refill = urllib.request.Request(f'{base_url}/api/refill-hearts', data=b'{}', headers={'Content-Type': 'application/json'})
res_refill = json.loads(opener.open(req_refill).read().decode('utf-8'))
print('7. Can Yenileme Testi:', res_refill)
assert res_refill['hearts'] == 5

print('\n*** TÜM TESTLER BAŞARIYLA GEÇTİ! ***')
