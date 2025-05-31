import pandas as pd
from datetime import datetime, timedelta

# Load the attendance data
attendance_data = pd.read_csv('attendance.csv')

# Display the data in a tabular format
print(attendance_data)

# Check for logins within 50 minutes
for i in range(1, len(attendance_data)):
    current_time = datetime.strptime(attendance_data['Time'][i], '%Y-%m-%d %H:%M:%S')
    previous_time = datetime.strptime(attendance_data['Time'][i-1], '%Y-%m-%d %H:%M:%S')
    
    if current_time - previous_time <= timedelta(minutes=50):
        print("Thank you for logging in within 50 minutes!")
        time_left = timedelta(minutes=50) - (current_time - previous_time)
        print(f"Try again after {time_left} to complete the 50 minutes.")
