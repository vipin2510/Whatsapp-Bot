import base64
import numpy as np
from flask import Flask, request, jsonify
import face_recognition
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
from PIL import Image
import mysql.connector

app = Flask(__name__)
app.debug = True
app.config['UPLOAD_FOLDER'] = 'uploads'
CORS(app)


def databaseRead(face_encodings):
    global result
    # Connect to the MySQL database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Vipin2510@",
        database="TRACKFLIX"
    )

    # Create a cursor object to execute SQL queries
    cursor = db.cursor()

    # Load the input image
    # input_image = face_recognition.load_image_file("DI_1689486038386.jpeg")

    # Detect faces in the input image
    # input_face_locations = face_recognition.face_locations(input_image)

    input_face_encodings = face_encodings

    # Retrieve known face encodings from the database
    cursor.execute(
        "SELECT face_encodes, name,crime, aditional_info FROM criminals;")
    rows = cursor.fetchall()

    known_encodings = []
    names = []
    crimes = []
    additionalInfos = []
    matchedTimestamps = []

    for row in rows:
        encoding = np.frombuffer(row[0], dtype=np.float64)
        NAME = row[1]
        CRIME = row[2]
        ADITIONAL_INFO = row[3]
        # Add the face encoding and timestamp to the lists
        known_encodings.append(encoding)
        names.append(NAME)
        crimes.append(CRIME)
        additionalInfos.append(ADITIONAL_INFO)

    # Compare the input face with known faces
    for input_face_encoding in input_face_encodings:
        # Compare the input face encoding with all known face encodings
        matches = face_recognition.compare_faces(
            known_encodings, input_face_encoding)

        # Find the indexes of matching faces
        matching_indexes = [i for i, match in enumerate(matches) if match]

        for matching_index in matching_indexes:
            # Retrieve the name and detail for the matching face
            matching_name = names[matching_index]
            matching_crime = crimes[matching_index]
            matchingaditional_infos = additionalInfos[matching_index]
            matchedTimestamps.append(
                f"Matching face found at: {matching_name}")
            #return {"name": matching_name, "crime": matching_crime, "additionalInfo": matchingaditional_infos}
            
        
    if len(matchedTimestamps) > 0:
        return 1
    
    


def dbwrite(Y, Z, a, b):
    # connect to database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Vipin2510@",
        database="TRACKFLIX"
    )
    mycursor = mydb.cursor()
    query = "INSERT INTO criminals (face_encodes, name,crime, aditional_info) VALUES ( %s, %s, %s, %s)"
    values = (Y, Z, a, b)
    mycursor.execute(query, values)

    mydb.commit()
    mycursor.close()
    mydb.close()


def process_image(file_path):
    global result
    image = Image.open(file_path).convert('RGB')

    if os.path.isfile(file_path):
        # Open the image and convert it to RGB

        # Load the image into face_recognition librarys
        face_image = face_recognition.load_image_file(file_path)

        # Find faces in the image
        face_locations = face_recognition.face_locations(face_image, model='cnn')

        if len(face_locations) > 0:
            # Encode the first face found
            face_encodings = face_recognition.face_encodings(
                face_image, face_locations)
            # Perform actions with the face encoding
            return databaseRead(face_encodings)
        else:
            return 3
    else:
        return 4


@app.route('/dbwrite', methods=['POST'])
def process_image_route():
    fileName = request.form['fileName']
    file_path = os.path.abspath(fileName)

    # Check if the file exists and wait until it is fully saved
    while not os.path.exists(file_path):
        pass

    result = process_image(file_path)
    print(result)
    if (result == 0):
        return 'code ni'
    elif (result == 1):
        return 'success'
    elif (result == 2):
        return 'already exist'
    elif (result == 3):
        return 'no face in the image'
    elif (result == 4):
        return 'send the photo again'
    else:
        return jsonify(result)


@app.route('/store', methods=['POST'])
def store():
    # Connect to the MySQL database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Vipin2510@",
        database="TRACKFLIX"
    )

    # Create a cursor object to execute SQL queries
    cursor = db.cursor()
    file_path = request.form['fileName']
    name = request.form['name']
    crime = request.form['crime']
    additionalInfo = request.form['additionalInfo']
    image = Image.open(file_path).convert('RGB')
    if os.path.isfile(file_path):
        # Open the image and convert it to RGB

        # Load the image into face_recognition librarys
        face_image = face_recognition.load_image_file(file_path)

        # Find faces in the image
        face_locations = face_recognition.face_locations(face_image, model='cnn')

        if len(face_locations) > 0:
            # Encode the first face found
            face_encodings = face_recognition.face_encodings(
                face_image, face_locations)[0]
            dbwrite(face_encodings.tobytes(), name, crime, additionalInfo)
            return "Succesfully Stored"
    return "Failed!"


@app.route('/dbsearch', methods=['POST'])
def dbsearch():
    # connect to database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Vipin2510@",
        database="TRACKFLIX"
    )
    mycursor = mydb.cursor()
    mycursor.execute("select face_encodes from criminals")
    rows = mycursor.fetchall()

    # Load the image into face_recognition librarys
    fileName = request.form['file']
    face_image = face_recognition.load_image_file(fileName)

    # # Find faces in the image
    face_locations = face_recognition.face_locations(face_image, model='cnn')
    face_encodings = face_recognition.face_encodings(
        face_image, face_locations)
    known_encodings = []
    names = []
    crimes = []
    additionalInfos = []
    matchedTimestamps = []

    for row in rows:
        # Compare the input face encoding with all known face encodings
        face_encoding = np.frombuffer(row[0], dtype=np.float64)
        known_encodings.append(face_encoding)
        # NAME = row[1]
        # CRIME = row[2]
        # ADITIONAL_INFO = row[3]
        # Add the face encoding and timestamp to the lists
        known_encodings.append(face_encoding)
        # names.append(NAME)
        # crimes.append(CRIME)
        # additionalInfos.append(ADITIONAL_INFO)

    for input_face_encoding in face_encodings:
        # Compare the input face encoding with all known face encodings
        matches = face_recognition.compare_faces(
            known_encodings, input_face_encoding)

    # Find the indexes of matching faces
        matching_indexes = [i for i, match in enumerate(matches) if match]

        for matching_index in matching_indexes:
            # matching_name = names[matching_index]
            # matching_crime = crimes[matching_index]
            # matchingaditional_infos = additionalInfos[matching_index]
            # matchedTimestamps.append(
            #     f"Matching face found at: {matching_name}")
            # return {"name": matching_name, "crime": matching_crime, "additionalInfo": matchingaditional_infos}
            return "Face Matched!"
    mydb.commit()
    print('Record SEARCHED successfully')
    mycursor.close()
    mydb.close()

    if len(face_locations) == 0:
        return "no face in the image"
    
    return "Face not found in the database!"


if __name__ == '__main__':
    app.run(host="localhost", port=8000)
