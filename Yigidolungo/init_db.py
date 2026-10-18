import sqlite3
import json
import os
from curriculum_data import CURRICULUM_STEPS

DB_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        name TEXT,
        email TEXT UNIQUE,
        google_id TEXT UNIQUE,
        avatar TEXT,
        hearts INTEGER DEFAULT 5,
        max_hearts INTEGER DEFAULT 5,
        last_heart_loss_time TIMESTAMP DEFAULT NULL,
        is_premium INTEGER DEFAULT 0,
        xp INTEGER DEFAULT 0,
        streak INTEGER DEFAULT 1,
        daily_goal INTEGER DEFAULT 50,
        bio TEXT DEFAULT 'Her gün yeni bir İngilizce kelime öğreniyorum! 🌊🐻',
        referral_code TEXT UNIQUE,
        invited_count INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Migration check for users table
    cursor.execute('PRAGMA table_info(users)')
    user_cols = [c[1] for c in cursor.fetchall()]
    for col, col_type in [
        ('name', 'TEXT'),
        ('email', 'TEXT'),
        ('google_id', 'TEXT'),
        ('avatar', 'TEXT'),
        ('daily_goal', 'INTEGER DEFAULT 50'),
        ('bio', 'TEXT DEFAULT "İngilizce öğrenmeyi seviyorum!"'),
        ('last_heart_loss_time', 'TIMESTAMP DEFAULT NULL'),
        ('is_premium', 'INTEGER DEFAULT 0'),
        ('streak_count', 'INTEGER DEFAULT 0'),
        ('last_study_date', 'TEXT DEFAULT NULL'),
        ('referral_code', 'TEXT'),
        ('invited_count', 'INTEGER DEFAULT 0')
    ]:
        if col not in user_cols:
            cursor.execute(f'ALTER TABLE users ADD COLUMN {col} {col_type}')

    # Units table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS units (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        color TEXT DEFAULT '#0284c7',
        order_index INTEGER DEFAULT 1,
        order_num INTEGER DEFAULT 1,
        is_unlocked INTEGER DEFAULT 0
    )
    ''')

    cursor.execute('PRAGMA table_info(units)')
    unit_cols = [c[1] for c in cursor.fetchall()]
    if 'order_index' not in unit_cols:
        cursor.execute('ALTER TABLE units ADD COLUMN order_index INTEGER DEFAULT 1')
    if 'is_unlocked' not in unit_cols:
        cursor.execute('ALTER TABLE units ADD COLUMN is_unlocked INTEGER DEFAULT 0')

    # Lessons table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS lessons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        unit_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT DEFAULT '',
        is_exam INTEGER DEFAULT 0,
        difficulty INTEGER DEFAULT 1,
        icon TEXT DEFAULT 'star',
        xp_reward INTEGER DEFAULT 15,
        order_num INTEGER DEFAULT 1,
        FOREIGN KEY (unit_id) REFERENCES units(id)
    )
    ''')

    # Questions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lesson_id INTEGER NOT NULL,
        type TEXT NOT NULL,
        instruction TEXT NOT NULL,
        prompt_text TEXT NOT NULL,
        english_speech TEXT,
        options TEXT NOT NULL, -- JSON array of strings
        correct_answer TEXT NOT NULL, -- JSON array or string
        explanation TEXT,
        order_num INTEGER DEFAULT 1,
        FOREIGN KEY (lesson_id) REFERENCES lessons(id)
    )
    ''')

    # User progress table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        lesson_id INTEGER NOT NULL,
        completed INTEGER DEFAULT 0,
        score INTEGER DEFAULT 0,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, lesson_id),
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (lesson_id) REFERENCES lessons(id)
    )
    ''')

    # Clean default guest user setup
    cursor.execute('SELECT * FROM users WHERE id = 1')
    existing_guest = cursor.fetchone()
    if not existing_guest:
        cursor.execute('''
        INSERT INTO users (id, username, name, email, google_id, hearts, max_hearts, xp, streak, daily_goal, bio, referral_code, invited_count)
        VALUES (1, 'misafir', 'Misafir Öğrenci', NULL, NULL, 5, 5, 0, 1, 50, 'İngilizce öğrenmeye yeni başladım! 🐻', 'YGDMISAFIR', 0)
        ''')
    else:
        cursor.execute('''
        UPDATE users SET username='misafir', name='Misafir Öğrenci', email=NULL, google_id=NULL, hearts=5, max_hearts=5, xp=0, streak=1, referral_code=COALESCE(referral_code, 'YGDMISAFIR'), invited_count=COALESCE(invited_count, 0) WHERE id=1
        ''')

    # Seed Unit 1 with 70 authentic CEFR A1 sentences across 13 steps (130 questions total)
    cursor.execute('DELETE FROM questions')
    cursor.execute('DELETE FROM lessons')
    cursor.execute('DELETE FROM units')
    cursor.execute('DELETE FROM user_progress WHERE user_id = 1')

    cursor.execute('''
    INSERT INTO units (title, description, color, order_num, order_index, is_unlocked)
    VALUES ('Ünite 1: İngilizceye Başlangıç (7 Konu + 6 Sınav)', 'Temel Selamlaşma, Tanışma ve Günlük Kalıplar (13 Adım)', '#0284c7', 1, 1, 1)
    ''')
    unit1_id = cursor.lastrowid

    # Seed locked Units 2, 3, 4
    cursor.execute('''
    INSERT INTO units (title, description, color, order_num, order_index, is_unlocked)
    VALUES 
    ('Ünite 2: Günlük Yaşam & Zaman (A1.2)', 'Saatler, planlar, alışkanlıklar ve temel zaman kalıpları.', '#059669', 2, 2, 0),
    ('Ünite 3: Çevre & İnsanlar (A2.1)', 'Kişi ve mekan tasvirleri, sıfatlar ve temel diyaloglar.', '#d97706', 3, 3, 0),
    ('Ünite 4: Seyahat & Alışveriş (A2.2)', 'Yol tarifleri, sipariş verme, alışveriş ve seyahat kalıpları.', '#7c3aed', 4, 4, 0)
    ''')

    # Insert curriculum steps & questions from curriculum_data
    for step in CURRICULUM_STEPS:
        cursor.execute('''
        INSERT INTO lessons (unit_id, title, description, is_exam, difficulty, icon, xp_reward, order_num)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (unit1_id, step['title'], step['description'], step['is_exam'], step['difficulty'], step['icon'], step['xp'], step['order']))
        lesson_id = cursor.lastrowid

        for q_idx, q in enumerate(step['questions'], 1):
            q_type, instruction, prompt, speech, options, answer, explanation = q
            if q_type == 'word_order':
                instruction = 'Dinle ve cümleyi kur:'
                prompt = ''
            cursor.execute('''
            INSERT INTO questions (lesson_id, type, instruction, prompt_text, english_speech, options, correct_answer, explanation, order_num)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (lesson_id, q_type, instruction, prompt, speech, json.dumps(options, ensure_ascii=False),
                  json.dumps(answer, ensure_ascii=False) if isinstance(answer, list) else answer,
                  explanation, q_idx))

    print(f"Successfully populated {len(CURRICULUM_STEPS)} steps with EXACTLY 10 questions each (130 questions total).")

    conn.commit()
    conn.close()
    print("Database initialization complete.")

if __name__ == '__main__':
    init_db()
