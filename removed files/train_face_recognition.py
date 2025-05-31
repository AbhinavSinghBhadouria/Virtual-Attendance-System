import cv2
import os
import numpy as np
import face_recognition
import pickle

def train_model(dataset_path):
    known_face_encodings = []
    known_face_names = []

    for name in os.listdir(dataset_path):
        person_path = os.path.join(dataset_path, name)
        image_files = os.listdir(person_path)[:5]  # Limit to first 5 images for testing
        for image_name in image_files:
            image_path = os.path.join(person_path, image_name)
            image = face_recognition.load_image_file(image_path)
            print(f"Processing image: {image_path}, shape: {image.shape}")  # Debugging info
            face_encodings = face_recognition.face_encodings(image)

            if face_encodings:  # Check if any encodings were found
                known_face_encodings.append(face_encodings[0])
                known_face_names.append(name)
            else:
                print(f"No faces found in image: {image_path}")

    np.save('face_encodings.npy', known_face_encodings)
    np.save('face_names.npy', known_face_names)

    # Save the model as a pickle file
    model_path = 'virtual_attendance_system/models/face_recognition_model.pkl'
    os.makedirs(os.path.dirname(model_path), exist_ok=True)  # Ensure the directory exists
    with open(model_path, 'wb') as f:
        pickle.dump({'encodings': known_face_encodings, 'names': known_face_names}, f)

if __name__ == "__main__":
    dataset_path = 'dataset'
    train_model(dataset_path)
