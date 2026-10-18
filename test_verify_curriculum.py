import sqlite3
import json

conn = sqlite3.connect('database.db')
conn.row_factory = sqlite3.Row
questions = conn.execute('SELECT * FROM questions').fetchall()
print('Total questions in DB:', len(questions))
assert len(questions) == 130, f'Expected 130 questions, got {len(questions)}'

wo_count = 0
mc_count = 0
for q in questions:
    q_id = q['id']
    if q['type'] == 'word_order':
        wo_count += 1
        assert q['instruction'] == 'Dinle ve cümleyi kur:', f"Wrong instruction in question {q_id}: {q['instruction']}"
        assert q['prompt_text'] == '', f"Prompt text not empty in question {q_id}: {q['prompt_text']}"
        assert len(q['english_speech']) > 3, f"Missing english_speech in question {q_id}"
        ans = json.loads(q['correct_answer'])
        opts = json.loads(q['options'])
        for w in ans:
            assert w in opts, f"Answer word '{w}' not in options in question {q_id}"
    elif q['type'] == 'multiple_choice':
        mc_count += 1
        opts = json.loads(q['options'])
        assert len(opts) == 4, f"Expected 4 options in question {q_id}, got {len(opts)}"
        assert q['correct_answer'] in opts, f"Correct answer '{q['correct_answer']}' not in options in question {q_id}"
        assert len(q['explanation']) > 5, f"Explanation too short in question {q_id}"

print(f"Pedagogical Verification Passed 100%! {mc_count} multiple choice, {wo_count} word order questions verified.")
