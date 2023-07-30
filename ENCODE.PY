import mysql.connector

def process_video(Y,Z,a,b):
    # connect to database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Vipin2510@",
        database="TRACKFLIX"
    )
    mycursor = mydb.cursor()
    query = "INSERT INTO CRIMINAL (FACE_ENCODES,NAME,CRIME,ADITIONAL_INFO) VALUES (%s, %s, %s, %s)"
    
    values = (Y,Z,a,b)
    mycursor.execute(query, values)

    mydb.commit()
    print('Record inserted successfully')
    mycursor.close()
    mydb.close()

