from flask import Flask, request
import face_recognition
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
from PIL import Image
import mysql.connector
import cv2
import numpy as np

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
    face_encodings = face_recognition.face_encodings(image, face_locations)[0]
    return face_encodings

def process_image(file_path):
    face_location=get_face_locations(file_path)
    # Encode the first face found
    face_encoding = get_face_encodings(file_path,face_location)
    
    # Check if the face encoding already exists in the database
        
        # If the face encoding does not exist, insert the new record into the database
        # connect to the database
    mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Vipin2510@",
                database="TRACKFLIX"
           )
    mycursor = mydb.cursor()

        # Convert the face encoding to bytes and store it in the database as a hexadecimal string
    
    face_encoding_hex =face_encoding.tobytes()

    query = "INSERT INTO criminals (face_encodes, name,crime, additional_info) VALUES ( %s, %s, %s, %s)"

    values = (face_encoding_hex,'shub','vid','bhu')
    mycursor.execute(query, values)

    mydb.commit()
    mycursor.close()
    mydb.close()
    print('muh kholo')
    return 'User stored in the database.'
    
process_image("check2.jpeg")