import smtplib
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import time

DB_PATH = 'attendance.db'
EXPORT_FOLDER = '.'  # Current directory
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_USER = 'your_email@gmail.com'  # Replace with sender email
EMAIL_PASSWORD = 'your_email_password'  # Replace with sender email password or app password

def export_attendance_for_teacher(teacher_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get teacher email
    cursor.execute('SELECT email FROM teacher_manager WHERE teacher_id = ?', (teacher_id,))
    result = cursor.fetchone()
    if not result:
        print(f"No email found for teacher ID {teacher_id}")
        conn.close()
        return None
    email = result[0]

    # Query attendance for this teacher (login_holder_id)
    query = '''
    SELECT name, timestamp
    FROM attendance_log
    WHERE login_holder_id = ?
    ORDER BY name, timestamp
    '''
    df = pd.read_sql_query(query, conn, params=(teacher_id,))
    conn.close()

    if df.empty:
        print(f"No attendance records found for teacher ID {teacher_id}")
        return None

    # Filter duplicates within 50 minutes
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    filtered_rows = []
    last_logged = {}

    for _, row in df.iterrows():
        name = row['name']
        timestamp = row['timestamp']
        if name not in last_logged:
            filtered_rows.append(row)
            last_logged[name] = timestamp
        else:
            if timestamp - last_logged[name] > timedelta(minutes=50):
                filtered_rows.append(row)
                last_logged[name] = timestamp

    filtered_df = pd.DataFrame(filtered_rows)

    # Save to Excel
    filename = os.path.join(EXPORT_FOLDER, f"attendance_export_{teacher_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
    filtered_df.to_excel(filename, index=False)
    print(f"Exported attendance for teacher {teacher_id} to {filename}")
    return filename, email

def send_email(to_email, subject, body, attachment_path):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEBase('application', "octet-stream"))

    # Attach the file
    part = MIMEBase('application', "octet-stream")
    with open(attachment_path, 'rb') as file:
        part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(attachment_path)}"')
    msg.attach(part)

    # Connect and send email
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USER, to_email, msg.as_string())
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

def send_attendance_emails():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT teacher_id FROM teacher_manager')
    teacher_ids = [row[0] for row in cursor.fetchall()]
    conn.close()

    for teacher_id in teacher_ids:
        result = export_attendance_for_teacher(teacher_id)
        if result:
            filepath, email = result
            send_email(email, 'Daily Attendance Report', 'Please find attached the attendance report.', filepath)

if __name__ == "__main__":
    # Wait until 7 PM to send emails
    while True:
        now = datetime.now()
        if now.hour == 19 and now.minute == 0:
            send_attendance_emails()
            break
        time.sleep(30)
