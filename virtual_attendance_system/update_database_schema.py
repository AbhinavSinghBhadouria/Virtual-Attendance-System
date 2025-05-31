import sqlite3

def update_schema():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    # Check if login_holder_id column exists
    cursor.execute("PRAGMA table_info(attendance_log)")
    columns = [info[1] for info in cursor.fetchall()]
    if 'login_holder_id' not in columns:
        print("Adding login_holder_id column to attendance_log table.")
        cursor.execute("ALTER TABLE attendance_log ADD COLUMN login_holder_id TEXT")
        conn.commit()
    else:
        print("login_holder_id column already exists.")

    conn.close()

if __name__ == "__main__":
    update_schema()
