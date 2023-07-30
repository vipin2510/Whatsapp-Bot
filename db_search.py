from flask import Flask, request
import face_recognition
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import numpy as np
from PIL import Image
import mysql.connector

import face_recognition
import cv2
import numpy as np
import mysql.connector
import base64
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

image_path='bod.jpg'

def dbsearch():
    # connect to database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Vipin2510@",
        database="TRACKFLIX"
    )
    mycursor = mydb.cursor()
    mycursor.execute("select FACE_ENCODES from CRIMINALS")
    rows = mycursor.fetchall()
    
    # Load the image into face_recognition librarys
    
        # Find faces in the image
    face_locations_image =get_face_locations(image_path)
    face_encodings_image = get_face_encodings(image_path,face_locations_image)
    face_encodings_image_array = np.array(face_encodings_image)
    known_encodings = []
    

    
    for row in rows:
        # Compare the input face encoding with all known face encodings
        face_encoding = np.frombuffer(row[0], dtype=np.float64)
        
        
        known_encodings.append(face_encoding)
        
    
        
        
    results = face_recognition.compare_faces(known_encodings, face_encodings_image_array,tolerance=0.5)

    print(results)
        
    mydb.commit()
    print('Record SEARCHED successfully')
    mycursor.close()
    mydb.close()
dbsearch()