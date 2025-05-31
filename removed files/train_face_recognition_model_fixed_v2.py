import face_recognition
import os
import pickle

# Load images from the 'data_set' directory
image_dir = 'data_set'
known_face_encodings = []
known_face_names = []

# Loop through each image in the directory
for filename in os.listdir(image_dir):
    if filename.endswith(('.jpg', '.jpeg', '.png', '.heic', '.tiff')):
        # Load the image
        image_path = os.path.join(image_dir, filename)
        image = face_recognition.load_image_file(image_path)

        # Get the face encodings for the image
        face_encodings = face_recognition.face_encodings(image)

        # If a face is found, add the encoding and name
        if face_encodings:
            known_face_encodings.append(face_encodings[0])
            known_face_names.append(os.path.splitext(filename)[0])  # Use the filename as the name

# Save the encodings and names to a file
model_path = os.path.join(os.getcwd(), 'face_recognition_model.pkl')
with open(model_path, 'wb') as f:
    pickle.dump((known_face_encodings, known_face_names), f)

print(f"Model trained and saved as '{model_path}'.")
