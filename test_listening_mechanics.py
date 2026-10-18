import urllib.request
import json
import sqlite3

base_url = 'http://127.0.0.1:5000'

# 1. Fetch lesson 1 questions via API
conn = sqlite3.connect('database.db')
first_lesson_id = conn.execute('SELECT id FROM lessons WHERE order_num = 1').fetchone()[0]
conn.close()

resp = urllib.request.urlopen(f'{base_url}/api/lesson/{first_lesson_id}/questions')
data = json.loads(resp.read().decode('utf-8'))
questions = data['questions']

# Find word_order question (e.g. Question 2 in Step 1)
word_order_qs = [q for q in questions if q['type'] == 'word_order']
assert len(word_order_qs) > 0, 'Step 1 should have word_order question'
wo_q = word_order_qs[0]

print('1. Found word_order question in Step 1:')
print('   - ID:', wo_q['id'])
print('   - Instruction:', wo_q['instruction'])
print('   - Prompt text:', repr(wo_q['prompt_text']))
print('   - English speech:', repr(wo_q['english_speech']))

assert wo_q['instruction'] == 'Dinle ve cümleyi kur:', f"Expected 'Dinle ve cümleyi kur:', got {wo_q['instruction']}"
assert wo_q['prompt_text'] == '', f"Expected empty prompt_text, got {wo_q['prompt_text']}"
assert len(wo_q['english_speech']) > 0, "english_speech must not be empty"

# 2. Check JS files
with open('static/js/lesson.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

assert 'Dinle ve cümleyi kur:' in js_content, "Missing 'Dinle ve cümleyi kur:' in lesson.js"
assert 'isListening' in js_content, "Missing isListening logic in lesson.js"
assert 'listening-bubble' in js_content, "Missing listening-bubble class in lesson.js"
assert 'SpeechEngine.speak(q.english_speech' in js_content, "Missing SpeechEngine auto-speak in lesson.js"
print('2. Verified lesson.js has listening bubble, hidden text, and auto Web Speech API integration.')

# 3. Check quiz.js sync
with open('static/js/quiz.js', 'r', encoding='utf-8') as f:
    quiz_content = f.read()

assert quiz_content == js_content, "quiz.js and lesson.js should be identical"
print('3. Verified quiz.js is perfectly synced with lesson.js.')

# 4. Check lesson.html loads quiz.js
with open('templates/lesson.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

assert 'quiz.js' in html_content, "lesson.html should include quiz.js"
print('4. Verified lesson.html includes quiz.js.')

print('\n*** TÜM DİNLEME VE KELİME SIRALAMA TESTLERİ BAŞARIYLA TAMAMLANDI! ***')
