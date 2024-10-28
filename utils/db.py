import sqlite3

def init_db():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            user_id INTEGER UNIQUE,
            name TEXT,
            group_name TEXT,
            is_subscribed BOOLEAN DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def add_or_update_student(user_id, name, group_name):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO students (user_id, name, group_name)
        VALUES (?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET name=excluded.name, group_name=excluded.group_name
    ''', (user_id, name, group_name))
    conn.commit()
    conn.close()

def student_exists(user_id):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students WHERE user_id = ?', (user_id,))
    student = cursor.fetchone()
    conn.close()
    return student is not None

def get_student(user_id):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students WHERE user_id = ?', (user_id,))
    student = cursor.fetchone()
    conn.close()
    return student

def update_subscription_status(user_id, is_subscribed):
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE students SET is_subscribed = ? WHERE user_id = ?', (is_subscribed, user_id))
    conn.commit()
    conn.close()

def get_all_students():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    conn.close()
    return students
