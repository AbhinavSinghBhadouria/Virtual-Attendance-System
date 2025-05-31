import sqlite3

def view_attendance():
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance")
    rows = cursor.fetchall()
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Timestamp: {row[2]}")
    conn.close()

if __name__ == "__main__":
    view_attendance()  # Call the function to view attendance
