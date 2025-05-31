import pandas as pd
from datetime import datetime, timedelta
import cv2

# Load the attendance data
attendance_data = pd.read_csv('attendance.csv')
print("Attendance data loaded successfully.")

# Initialize camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Camera not accessible.")
    exit()

# Frame processing rate
frame_skip = 5  # Process every 5th frame
frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to read from camera.")
        break

    frame_count += 1
    if frame_count % frame_skip != 0:
        continue  # Skip processing for this frame

    # Check for logins within 50 minutes
    for i in range(1, len(attendance_data)):
        current_time = datetime.strptime(attendance_data['Time'][i], '%Y-%m-%d %H:%M:%S')
        previous_time = datetime.strptime(attendance_data['Time'][i-1], '%Y-%m-%d %H:%M:%S')
        
        if current_time - previous_time <= timedelta(minutes=50):
            message = "Thank you for logging in within 50 minutes!"
            time_left = timedelta(minutes=50) - (current_time - previous_time)
            message_time_left = f"Try again after {time_left}."
            
            # Display messages on the camera frame
            cv2.putText(frame, message, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, message_time_left, (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Show the frame
    cv2.imshow('Camera', frame)

    if cv2.waitKey(30) & 0xFF == ord('q'):  # Adjusted wait time
        break

cap.release()
cv2.destroyAllWindows()
