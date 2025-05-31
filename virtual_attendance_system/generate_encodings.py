import face_recognition
import os
import pickle

def generate_encodings():
    dataset_dir = './dataset'
    encodings = []
    names = []

    for person_name in os.listdir(dataset_dir):
        person_dir = os.path.join(dataset_dir, person_name)
        if not os.path.isdir(person_dir):
            continue
        for image_name in os.listdir(person_dir):
            image_path = os.path.join(person_dir, image_name)
            image = face_recognition.load_image_file(image_path)
            face_encs = face_recognition.face_encodings(image)
            if face_encs:
                encodings.append(face_encs[0])
                names.append(person_name)

    data = {'encodings': encodings, 'names': names}
    os.makedirs('encodings', exist_ok=True)
    with open('encodings/face_encodings.pkl', 'wb') as f:
        pickle.dump(data, f)
    print("Encodings generated and saved to encodings/face_encodings.pkl")

if __name__ == "__main__":
    generate_encodings()
