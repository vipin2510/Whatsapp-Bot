from flask import Flask, request
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

import mysql.connector

def is_face_encoding_exists(face_encoding):
    # Connect to the database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Vipin2510@",
        database="TRACKFLIX"
    )
    mycursor = mydb.cursor()

    # Fetch all the face encodings from the database
    query = "SELECT FACE_ENCODES FROM CRIMINAL"
    mycursor.execute(query)

    results = mycursor.fetchall()

    # Convert the results to a list of face encodings (from hexadecimal to bytes)
    existing_face_encodings = [bytes.fromhex(result[0].decode()) for result in results]

    # Compare the new face encoding with all the existing face encodings
    is_existing_user = any(face_recognition.compare_faces(existing_face_encodings, face_encoding))

    mycursor.close()
    mydb.close()

    return is_existing_user

def process_image(file_path):
    image = Image.open(file_path).convert('RGB')

    if os.path.isfile(file_path):
        # Open the image and convert it to RGB

        # Load the image into face_recognition librarys
        face_image = face_recognition.load_image_file(file_path)

        # Find faces in the image
        face_locations = face_recognition.face_locations(face_image)

        if len(face_locations) == 0:
            return 'No face found in the image.', 400

    # Encode the first face found
        face_encoding = face_recognition.face_encodings(image, face_locations)[0]
    
    # Check if the face encoding already exists in the database
        if is_face_encoding_exists(face_encoding):
            return 'User already stored in the database.'
        else:
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
            face_encoding_bytes = face_encoding.tobytes()
            face_encoding_hex = face_encoding_bytes.hex()

            query = "INSERT INTO CRIMINALS (FACE_ENCODES) VALUES (%s)"
            values = (face_encoding_hex,)
            mycursor.execute(query, values)

            mydb.commit()
            mycursor.close()
            mydb.close()

        return 'User stored in the database.'
    
@app.route('/process_image', methods=['POST'])
def process_image_route():
    fileName = request.form['fileName']
    file_path = os.path.abspath(fileName)

    # Check if the file exists and wait until it is fully saved
    while not os.path.exists(file_path):
        pass

    process_image(file_path)

    return 'File received and processed successfully!'


if __name__ == '__main__':
    app.run(host="localhost", port=8000)