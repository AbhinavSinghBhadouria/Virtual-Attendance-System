import sqlite3

def list_students():
    try:
        conn = sqlite3.connect('attendance.db')
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT name FROM attendance")
        rows = cursor.fetchall()
        print("Students in database:")
        for row in rows:
            print(f"'{row[0]}'")
    except Exception as e:
        print(f"Error listing students: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    list_students()
