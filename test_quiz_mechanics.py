import urllib.request
import json
import http.cookiejar

base_url = 'http://127.0.0.1:5000'

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# 1. Login demo as standard user
opener.open(f'{base_url}/login/demo?user=standard')

# Refill hearts & reset progress
req_refill = urllib.request.Request(f'{base_url}/api/refill-hearts', data=b'{}', headers={'Content-Type': 'application/json'})
opener.open(req_refill)

# 2. Check all 13 steps have exactly 10 questions
import sqlite3
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('SELECT l.order_num, l.title, COUNT(q.id) FROM lessons l JOIN questions q ON l.id = q.lesson_id GROUP BY l.id ORDER BY l.order_num ASC')
steps = cursor.fetchall()
print('1. Soru Sayısı Kontrolü (13 Adım):')
assert len(steps) == 13, f'Expected 13 steps, got {len(steps)}'
for s in steps:
    safe_title = s[1].encode('ascii', 'ignore').decode('ascii')
    print(f'   Step {s[0]}: {s[2]} soru -> {safe_title}')
    assert s[2] == 10, f'Step {s[0]} does not have 10 questions!'

cursor.execute('SELECT COUNT(*) FROM questions')
total_q = cursor.fetchone()[0]
print(f'   -> Toplam soru sayısı: {total_q} (Hedef: 130).')
assert total_q == 130, f'Expected 130 total questions, got {total_q}'

# 3. Test Question 1 API response
# Get lesson 1 ID (order_num = 1)
cursor.execute('SELECT id FROM lessons WHERE order_num = 1')
lesson1_id = cursor.fetchone()[0]

resp_q = opener.open(f'{base_url}/api/lesson/{lesson1_id}/questions')
q_data = json.loads(resp_q.read().decode('utf-8'))
questions = q_data['questions']
assert len(questions) == 10, f'API returned {len(questions)} questions instead of 10!'
print(f'2. Ders 1 Soru API testi: Tam 10 soru başarıyla döndü.')

# 4. Test Wrong Answer (Heart deduction & evaluation)
q1 = questions[0]
wrong_payload = json.dumps({'question_id': q1['id'], 'answer': 'Tamamen Yanlış Şık'}).encode('utf-8')
req_wrong = urllib.request.Request(f'{base_url}/api/check-answer', data=wrong_payload, headers={'Content-Type': 'application/json'})
res_wrong = json.loads(opener.open(req_wrong).read().decode('utf-8'))
print('3. Yanlış Cevap Yanıtı (Can Düşme):', res_wrong)
assert res_wrong['is_correct'] is False, 'Should be evaluated as incorrect'
assert res_wrong['hearts'] == 4, f'Expected 4 hearts, got {res_wrong["hearts"]}'
assert 'explanation' in res_wrong, 'Explanation hint missing'

# 5. Test Correct Answer
_corr = conn.execute('SELECT correct_answer FROM questions WHERE id = ?', (q1['id'],)).fetchone()[0]
conn.close()

correct_payload = json.dumps({'question_id': q1['id'], 'answer': _corr}).encode('utf-8')
req_correct = urllib.request.Request(f'{base_url}/api/check-answer', data=correct_payload, headers={'Content-Type': 'application/json'})
res_correct = json.loads(opener.open(req_correct).read().decode('utf-8'))
print('4. Doğru Cevap Yanıtı:', res_correct)
assert res_correct['is_correct'] is True, 'Should be evaluated as correct'

print('\n*** TÜM QUIZ MEKANİĞİ VE 10 SORULUK STANDART TESTLERİ BAŞARIYLA GEÇTİ! ***')

