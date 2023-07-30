-- Active: 1690657274571@@127.0.0.1@3306@TRACKFLIX
import numpy as np
import cv2
import face_recognition
from retinaface import RetinaFace

# Data to be appended to the file

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

user_name = "dady"
user_age = "Enter your age: "
user_face_encodes = "Enter your location: "

# Data to be written to the file
data = f"Name: {user_name}\nAge: {user_age}\nLocation: {user_location}\n"
file_path = "example.txt"
print("Vipin gandu")

# Open the file in append mode ('a')
# This will create a new file if it doesn't exist or append to the existing content.
with open(file_path, 'a') as file:
    # Write the data to the file
    file.write(data)

print("Details have been added to the file.")
