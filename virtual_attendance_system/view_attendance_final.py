import pandas as pd
from datetime import datetime, timedelta

# Load the attendance data
attendance_data = pd.read_csv('attendance.csv')

# Display the data in a tabular format
print(attendance_data)

# Check for logins within 50 minutes
current_time = pd.to_datetime(attendance_data['Time'])
previous_time = current_time.shift(1)

# Calculate time differences
time_diff = current_time - previous_time

# Identify logins within 50 minutes
within_50_minutes = time_diff <= timedelta(minutes=50)

for i in range(1, len(attendance_data)):
    if within_50_minutes[i]:
        print("Thank you for logging in within 50 minutes!")
        time_left = timedelta(minutes=50) - time_diff[i]
        print(f"Try again after {time_left}.")
        print(f"You can log in again at: {current_time[i] + time_left}.")
