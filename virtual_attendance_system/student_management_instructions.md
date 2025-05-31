# Student Management Instructions

This document explains how to manage student records in the virtual attendance system database (`attendance.db`).

---

## 1. Viewing Students

To view all students currently in the database, you can run the following Python script:

```python
import sqlite3

conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()
cursor.execute("SELECT id, name FROM attendance")
rows = cursor.fetchall()
for row in rows:
    print(f"ID: {row[0]}, Name: {row[1]}")
conn.close()
```

---

## 2. Deleting a Student Record

To delete a student record from the database, you need to remove their entries from both the `attendance_log` and `attendance` tables.

### SQL Commands

```sql
DELETE FROM attendance_log WHERE name = 'Student Name';
DELETE FROM attendance WHERE name = 'Student Name';
```

You can execute these commands using a SQLite client or via Python.

### Python Script Example

```python
import sqlite3

def delete_student(name):
    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM attendance_log WHERE name = ?", (name,))
    cursor.execute("DELETE FROM attendance WHERE name = ?", (name,))
    conn.commit()
    conn.close()

# Example usage
delete_student('John Doe')
```

---

## 3. Important Notes

- Always ensure you have a backup of your database before deleting records.
- Deleting a student will remove all their attendance logs and face encoding data.
- Use the exact student name as stored in the database to avoid accidental deletions.

---

If you need assistance with managing student records or automating these tasks, feel free to ask.
