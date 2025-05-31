# Teacher/Manager Database Management Instructions

This document explains how to manage the teacher/manager records in the attendance system database (`attendance.db`). These records are essential for sending attendance reports via email after 7 PM.

---

## 1. Adding a Teacher/Manager

To add a new teacher or manager, you need to insert their details into the `teacher_manager` table. The required fields are:

- **name**: Full name of the teacher/manager.
- **teacher_id**: Unique identifier for the teacher/manager.
- **email**: Email address where attendance reports will be sent.

### Using Python Script

You can use the following Python script to add a teacher/manager:

```python
from teacher_manager_db import add_teacher_manager

# Example: Add a teacher
add_teacher_manager('John Doe', 'T123', 'john.doe@example.com')
```

Run this script in your project environment to add the record.

---

## 2. Viewing Teacher/Manager Records

You can view the existing records using any SQLite database viewer or by running a simple Python script:

```python
import sqlite3

conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM teacher_manager')
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()
```

---

## 3. Removing a Teacher/Manager

To remove a teacher/manager from the database, execute the following SQL command:

```sql
DELETE FROM teacher_manager WHERE teacher_id = 'T123';
```

You can run this command using a SQLite client or via Python:

```python
import sqlite3

conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()
cursor.execute("DELETE FROM teacher_manager WHERE teacher_id = ?", ('T123',))
conn.commit()
conn.close()
```

---

## 4. Updating Teacher/Manager Details

To update email or name, use the following SQL command:

```sql
UPDATE teacher_manager SET email = 'new.email@example.com' WHERE teacher_id = 'T123';
```

Or via Python:

```python
import sqlite3

conn = sqlite3.connect('attendance.db')
cursor = conn.cursor()
cursor.execute("UPDATE teacher_manager SET email = ? WHERE teacher_id = ?", ('new.email@example.com', 'T123'))
conn.commit()
conn.close()
```

---

## 5. How Attendance Report Emailing Works

- The system exports attendance records associated with each teacher/manager's `teacher_id`.
- After 7 PM daily, the system automatically sends the attendance Excel report to the email address stored for each teacher/manager.
- Ensure the `teacher_manager` table is up to date with correct email addresses for successful delivery.

---

## 6. Additional Notes

- Make sure to keep the `teacher_id` unique for each teacher/manager.
- The email sending functionality requires valid SMTP credentials configured in `send_attendance_email.py`.
- For any changes in email credentials or SMTP server, update the configuration in `send_attendance_email.py`.

---

If you need assistance with any of these steps, feel free to ask.
