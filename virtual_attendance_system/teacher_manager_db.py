import sqlite3

def create_teacher_manager_table():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teacher_manager (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            teacher_id TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def add_teacher_manager(name, teacher_id, email):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO teacher_manager (name, teacher_id, email)
        VALUES (?, ?, ?)
    ''', (name, teacher_id, email))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_teacher_manager_table()
