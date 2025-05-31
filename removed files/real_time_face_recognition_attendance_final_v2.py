import face_recognition
import pickle
import cv2
import numpy as np
import datetime

# Load the saved face encodings and labels
with open('face_recognition_model.pkl', 'rb') as f:
    face_encodings, face_labels = pickle.load(f)

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Initialize attendance list
attendance_list = []

print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Convert the image from BGR to RGB
    rgb_frame = frame[:, :, ::-1]

    # Find all face locations and encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings_in_frame = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left) in face_locations:
        if len(face_encodings_in_frame) > 0:  # Check if there are any encodings found
            face_encoding = face_encodings_in_frame[0]  # Use the first encoding found
            # Compare the face encoding with the known encodings
            matches = face_recognition.compare_faces(face_encodings, face_encoding)
            name = "Unknown"

            # Use the first match found
            if True in matches:
                first_match_index = matches.index(True)
                name = face_labels[first_match_index]

                # Mark attendance if the person is recognized and not already in the list
                if name not in attendance_list:
                    attendance_list.append(name)
                    print(f"Attendance marked for: {name} at {datetime.datetime.now()}")

            # Draw a rectangle around the face and label it
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Display the resulting frame
    cv2.imshow("Face Recognition Attendance", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()

# Save attendance to a file
with open('attendance_record.txt', 'w') as f:
    for name in attendance_list:
        f.write(f"{name} - {datetime.datetime.now()}\n")

print("Attendance has been recorded.")
