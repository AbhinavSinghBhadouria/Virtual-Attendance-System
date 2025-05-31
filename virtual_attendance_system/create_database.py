import sqlite3
import os
import pickle

def create_database():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    # Create table if it doesn't exist for face encodings
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            encoding BLOB NOT NULL
        )
    ''')

    # Create table if it doesn't exist for attendance logs with login_holder_id
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            login_holder_id TEXT
        )
    ''')

    conn.commit()
    return conn, cursor

def insert_face(name, encoding):
    conn, cursor = create_database()
    cursor.execute('INSERT INTO attendance (name, encoding) VALUES (?, ?)', (name, encoding))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # The insert_face function expects encoding, but main.py uses attendance_log for attendance
    # So this script should only create tables and not insert face encodings
    create_database()
    # Comment out or remove the following lines that cause errors
    # names, encodings = load_encodings()
    # for name, encoding in zip(names, encodings):
    #     insert_face(name, encoding)

# Remove or comment out the call to insert_face outside main guard to prevent execution on import
# insert_face(name encoding)

def load_encodings():
    encodings_path = 'encodings/face_encodings.pkl'
    with open(encodings_path, 'rb') as f:
        data = pickle.load(f)
    return data['encodings'], data['names']

if __name__ == "__main__":
    # Commented out to prevent execution errors
    pass
