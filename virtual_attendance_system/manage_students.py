import sqlite3

def delete_student(name, roll_no):
    """
    Delete a student record from attendance_log, attendance, and dataset folders by name and roll number.
    """
    try:
        conn = sqlite3.connect('attendance.db')
        cursor = conn.cursor()
        # Delete from attendance_log
        cursor.execute("DELETE FROM attendance_log WHERE name = ?", (name,))
        # Delete from attendance
        cursor.execute("DELETE FROM attendance WHERE name = ?", (name,))
        conn.commit()
        print(f"Deleted student records for: {name} with roll no: {roll_no}")
    except Exception as e:
        print(f"Error deleting student records: {e}")
    finally:
        conn.close()

    # Delete student's images folder if exists
    import shutil
    import os
    dataset_path = f"./dataset/{name} {roll_no}"
    if os.path.exists(dataset_path):
        try:
            shutil.rmtree(dataset_path)
            print(f"Deleted dataset folder: {dataset_path}")
        except Exception as e:
            print(f"Error deleting dataset folder: {e}")

import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python manage_students.py <name> <roll_no>")
        sys.exit(1)
    name = sys.argv[1]
    roll_no = sys.argv[2]
    delete_student(name, roll_no)

if __name__ == "__main__":
    main()
