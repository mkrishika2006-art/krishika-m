import face_recognition
import numpy as np

def get_face_embedding(file_path):
    image = face_recognition.load_image_file(file_path)
    face_locations = face_recognition.face_locations(image)
    if len(face_locations) == 0:
        return None
    embedding = face_recognition.face_encodings(image, known_face_locations=face_locations)[0]
    return embedding.tolist()

def compare_faces(known_embedding, unknown_embedding, tolerance=0.5):
    return face_recognition.compare_faces([np.array(known_embedding)], np.array(unknown_embedding), tolerance=tolerance)[0]
