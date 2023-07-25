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

app = Flask(__name__)
app.debug = True
# app.config['UPLOAD_FOLDER'] = 'uploads'
# CORS(app)


@app('/process_image', methods=['pOST'])
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
    face_image = face_recognition.load_image_file('DI_1690047254910.jpeg')

        # Find faces in the image
    face_locations = face_recognition.face_locations(face_image)
    face_encodings = face_recognition.face_encodings(face_image, face_locations)
    known_encodings = []
    if len(face_locations) > 0:
            # Encode the first face found
        
        #print(type(face_encoding))   

    
     for row in rows:
        # Compare the input face encoding with all known face encodings
        encoding_base64 = row[0]
        known_encodings.append(face_encoding)
        face_encoding = np.frombuffer(base64.b64decode(encoding_base64), dtype=np.float64)
        known_encodings.append(face_encoding)
        
    for input_face_encoding in face_encodings:
    # Compare the input face encoding with all known face encodings
        matches = face_recognition.compare_faces(known_encodings, input_face_encoding)
    
    # Find the indexes of matching faces
        matching_indexes = [i for i, match in enumerate(matches) if match]
    
        for matching_index in matching_indexes:
        
        
            print("Matching face found at:")

        
    mydb.commit()
    print('Record SEARCHED successfully')
    mycursor.close()
    mydb.close()
