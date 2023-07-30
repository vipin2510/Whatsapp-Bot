import numpy as np
import cv2
import face_recognition
from retinaface import RetinaFace

def get_face_locations(image_path):
    image = cv2.imread(image_path)
    faces = RetinaFace.detect_faces(image)
    face_locations = []
    for face in faces.values():
       x1, y1, x2, y2 = face['facial_area']
       face_locations.append((y1, x2, y2, x1))  # Convert RetinaFace format to face_recognition format
    return face_locations

def get_face_encodings(image_path, face_locations):
    image = face_recognition.load_image_file(image_path)
    face_encodings = face_recognition.face_encodings(image, face_locations)

    return face_encodings
ty
if __name__ == "__main__":
    input_image_path = "check1.jpeg"
    inputa = "check2.jpeg"
    face_locationa = get_face_locations(inputa)
    # Step 1: Get face locations using RetinaFace
    face_locations = get_face_locations(input_image_path)
    # print(face_locations)
    # Step 2: Get face encodings using face_recognition
    face_encodings = get_face_encodings(input_image_path, face_locations)
    face_encodingsa = get_face_encodings(inputa,face_locationa)
    face_encodings = np.array(face_encodings)
    face_encodingsa = np.array(face_encodingsa)
    print
    results = face_recognition.compare_faces(face_encodings, face_encodingsa,tolerance=0.5)

    # Step 3: Print the comparison result
    if True in results:
        print("The images are of the same person.")
    else:
        print("The images are of different people.")
