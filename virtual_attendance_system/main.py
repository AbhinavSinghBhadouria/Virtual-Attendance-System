import face_recognition
import cv2
import numpy as np
import pickle
import pandas as pd
import os
import sqlite3
from datetime import datetime
from geopy.geocoders import Nominatim

def load_encodings():
    with open('encodings/face_encodings.pkl', 'rb') as f:
        data = pickle.load(f)
    return data['encodings'], data['names']

def log_attendance(name, latitude, longitude, login_holder_id=None):
    try:
        print(f"Attempting to log attendance for: {name}")
        conn = sqlite3.connect('attendance.db')
        cursor = conn.cursor()

        # Check if the name is already logged within the last 50 minutes
        cursor.execute('''
            SELECT * FROM attendance_log WHERE name = ? AND datetime(timestamp) > datetime('now', '-50 minutes')
        ''', (name,))
        
        if cursor.fetchone() is None:  # No recent entry found
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if login_holder_id:
                cursor.execute('''
                    INSERT INTO attendance_log (name, timestamp, login_holder_id) VALUES (?, ?, ?)
                ''', (name, current_time, login_holder_id))
            else:
                cursor.execute('''
                    INSERT INTO attendance_log (name, timestamp) VALUES (?, ?)
                ''', (name, current_time))
            conn.commit()
            print(f"Logged attendance for: {name} at {current_time}")
        else:
            print(f"Attendance for {name} already logged recently.")
        
        conn.close()
    except Exception as e:
        print(f"Error logging attendance: {e}")

def get_latitude():
    # Placeholder for actual latitude retrieval logic
    return 12.34  # Replace with actual latitude retrieval method

def get_longitude():
    # Placeholder for actual longitude retrieval logic
    return 56.78  # Replace with actual longitude retrieval method

def get_location(latitude, longitude):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse((latitude, longitude), language='en')
    return location.address if location else "Location not found"

def recognize_faces():
    encodings, names = load_encodings()
    cap = None
    recognized_once = False

    # Prompt for login holder (teacher/manager) ID
    login_holder_id = input("Enter your teacher/manager ID: ").strip()

    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open video capture device.")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Warning: Failed to read frame from camera.")
                break

            try:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Resize frame for faster processing
                small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.25, fy=0.25)
                face_locations = face_recognition.face_locations(small_frame)
                face_encodings = face_recognition.face_encodings(small_frame, face_locations)
            except Exception as e:
                print(f"Error during face detection/encoding: {e}")
                continue

            if len(face_locations) > 1:
                # Display ERROR INTERRUPT on the frame
                cv2.putText(frame, "ERROR INTERRUPT", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
            else:
                for face_encoding, face_location in zip(face_encodings, face_locations):
                    distances = face_recognition.face_distance(encodings, face_encoding)
                    print(f"Face distances: {distances}")  # Log all distances for analysis
                    min_distance = np.min(distances) if len(distances) > 0 else None
                    threshold = 0.45  # Stricter threshold for better accuracy
                    name = "Unknown"
                    if min_distance is not None and min_distance < threshold:
                        matched_idx = np.argmin(distances)
                        name = names[matched_idx]
                        latitude = get_latitude()  # Replace with actual latitude retrieval method
                        longitude = get_longitude()  # Replace with actual longitude retrieval method
                        print(f"Recognized: {name} with distance: {min_distance}")
                        log_attendance(name, latitude, longitude, login_holder_id)
                        print(f"Logged attendance for: {name} at latitude: {latitude}, longitude: {longitude}")
                        recognized_once = True
                        break  # Exit the for loop after first recognition

                    top, right, bottom, left = face_location
                    # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            cv2.imshow('Face Recognition', frame)
            if recognized_once or (cv2.waitKey(1) & 0xFF == ord('q')):
                break

    except Exception as e:
        print(f"Unexpected error: {e}")

    finally:
        if cap:
            cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    recognize_faces()
