import numpy as np
import sqlite3
import base64

# Sample NumPy ndarray
data = np.array([[1, 2, 3], [4, 5, 6]])

# Step 1: Serialize the ndarray and convert to base64 string
serialized_data = np.savez_compressed('serialized_data.npz', data=data)
with open('serialized_data.npz', 'rb') as f:
    base64_data = base64.b64encode(f.read())

# Step 2: Connect to the SQLite database and create a table
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS my_table (id INTEGER PRIMARY KEY, data BLOB)''')

# Step 3: Insert the serialized data into the table
cursor.execute('INSERT INTO my_table (data) VALUES (?)', (base64_data,))

# Commit the changes and close the connection
conn.commit()
conn.close()

# Step 4: Retrieve the ndarray from the SQL table
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()
cursor.execute('SELECT data FROM my_table WHERE id = 1')
base64_data = cursor.fetchone()[0]
serialized_data = base64.b64decode(base64_data)
npzfile = np.load(id.BytesIO(serialized_data))
retrieved_data = npzfile['data']

print(retrieved_data)
