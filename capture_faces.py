import cv2
import os
import sqlite3

def is_person_logged(name, roll_no):
    try:
        conn = sqlite3.connect('attendance.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM attendance_log WHERE name = ?', (name,))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except Exception as e:
        print(f"Error checking attendance log: {e}")
        return False

def capture_faces(person_name, roll_no, num_images=20):
    if is_person_logged(person_name, roll_no):
        print(f"Error: Person with name '{person_name}' or roll number '{roll_no}' is already in the attendance log.")
        return

    dataset_dir = 'dataset'
    person_dir = os.path.join(dataset_dir, f"{person_name}_{roll_no}")
    os.makedirs(person_dir, exist_ok=True)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print(f"Starting face capture for {person_name} (Roll No: {roll_no}). Automatic capture every 10 frames. Press 'q' to quit early.")
    count = 0
    frame_count = 0
    while count < num_images:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame from webcam.")
            break

        cv2.imshow('Capture Faces - Automatic capture every 10 frames, q to quit', frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            print("Quitting face capture.")
            break

        frame_count += 1
        if frame_count % 10 == 0:
            img_path = os.path.join(person_dir, f'{count+1}.jpg')
            cv2.imwrite(img_path, frame)
            print(f"Captured image {count+1} for {person_name} (Roll No: {roll_no})")
            count += 1

    cap.release()
    cv2.destroyAllWindows()
    print(f"Captured {count} images for {person_name} (Roll No: {roll_no})")

if __name__ == "__main__":
    person_name = input("Enter the name of the person to capture faces for: ")
    roll_no = input("Enter the roll number of the person: ")
    capture_faces(person_name, roll_no)
