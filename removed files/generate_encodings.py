import face_recognition
import os
import pickle

def encode_faces():
    dataset_path = 'dataset'
    encodings_path = 'encodings/face_encodings.pkl'
    known_encodings = []
    known_names = []

    for person_name in os.listdir(dataset_path):
        person_path = os.path.join(dataset_path, person_name)
        if os.path.isdir(person_path):
            for image_name in os.listdir(person_path):
                image_path = os.path.join(person_path, image_name)
                image = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(image)
                if encodings:
                    known_encodings.append(encodings[0])
                    known_names.append(person_name)

    with open(encodings_path, 'wb') as f:
        pickle.dump({'encodings': known_encodings, 'names': known_names}, f)

if __name__ == "__main__":
    encode_faces()
