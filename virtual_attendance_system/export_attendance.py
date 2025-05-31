import sqlite3
import pandas as pd
from datetime import datetime, timedelta

def export_attendance_to_excel():
    try:
        conn = sqlite3.connect('attendance.db')
        query = '''
        SELECT name, timestamp
        FROM attendance_log
        ORDER BY name, timestamp
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()

        # Convert timestamp column to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Filter out duplicate entries within 50 minutes for the same person
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
                else:
                    # Duplicate within 50 minutes, skip
                    pass

        filtered_df = pd.DataFrame(filtered_rows)

        # Save to Excel file with timestamped filename
        filename = f"attendance_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        filtered_df.to_excel(filename, index=False)
        print(f"Attendance exported successfully to {filename}")

    except Exception as e:
        print(f"Error exporting attendance: {e}")

if __name__ == "__main__":
    export_attendance_to_excel()
