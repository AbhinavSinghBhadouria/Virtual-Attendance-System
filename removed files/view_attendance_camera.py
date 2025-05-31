import pandas as pd
from datetime import datetime, timedelta
import cv2

# Load the attendance data
attendance_data = pd.read_csv('attendance.csv')

# Initialize camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Display the data in a tabular format (if needed)
    # You can add code here to display the attendance data on the frame if required

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

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
