import face_recognition
import pickle
import cv2
import dlib

# Load the saved face encodings and labels
with open('face_recognition_model.pkl', 'rb') as f:
    face_encodings, face_labels = pickle.load(f)

# Initialize the webcam
cap = cv2.VideoCapture(0)

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
    face_landmarks = face_recognition.face_landmarks(rgb_frame, face_locations)
    face_encodings_in_frame = face_recognition.face_encodings(rgb_frame, face_landmarks, num_jitters=1)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings_in_frame):
        # Compare the face encoding with the known encodings
        matches = face_recognition.compare_faces(face_encodings, face_encoding)
        name = "Unknown"

        # Use the first match found
        if True in matches:
            first_match_index = matches.index(True)
            name = face_labels[first_match_index]

        # Draw a rectangle around the face and label it
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Display the resulting frame
    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
