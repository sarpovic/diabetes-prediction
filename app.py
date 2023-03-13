"""
This is a Flask API that uses a trained Random Forest model to predict whether a person has diabetes or not.

The API has two routes:

'/' : This is the home page which renders an HTML template for user input.
'/predict': This route accepts a POST request with user input data, predicts the outcome using a trained Random Forest model, and renders an HTML template displaying the prediction along with the previously made predictions.
The 'predict' route saves each prediction in an SQLite database with additional columns for the date and time of the prediction.

Dependencies:

Flask
pickle
numpy
sqlite3
datetime
Functions:

home(): Renders an HTML template for user input.
predict(): Accepts a POST request with user input data, predicts the outcome using a trained Random Forest model, and renders an HTML template displaying the prediction along with the previously made predictions. It also saves each prediction in an SQLite database.
Example Usage:

Run the Flask API:
$ python app.py

Access the home page:
http://localhost:5000/

Enter the required input fields:
pregnancies, glucose, bloodpressure, skinthickness, insulin, bmi, dpf, age

Click on the 'Predict' button to see the prediction result.

The 'Previous Predictions' section below the prediction result will show all the previous predictions.
"""

from flask import Flask, render_template, request
import pickle
import numpy as np
import sqlite3
from datetime import datetime

filename = 'randomforest.pkl'
classifier = pickle.load(open(filename, 'rb'))

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        preg = int(request.form['pregnancies'])
        glucose = int(request.form['glucose'])
        bp = int(request.form['bloodpressure'])
        st = int(request.form['skinthickness'])
        insulin = int(request.form['insulin'])
        bmi = float(request.form['bmi'])
        dpf = float(request.form['dpf'])
        age = int(request.form['age'])
        
        data = np.array([[preg, glucose, bp, st, insulin, bmi, dpf, age]])
        my_prediction = classifier.predict(data)
        my_prediction = int.from_bytes(my_prediction, byteorder='little')

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS kayitlar
             (pregnancies INTEGER, glucose INTEGER, bloodpressure INTEGER, 
              skinthickness INTEGER, insulin INTEGER, bmi REAL, dpf REAL, age INTEGER,my_prediction INT, prediction_time TIMESTAMP)''')
        

        now = datetime.now().strftime("%d-%m-%Y")
        c.execute("INSERT INTO kayitlar VALUES (?, ?, ?, ?, ?, ?, ?, ?,? ,?)", (preg, glucose, bp, st, insulin, bmi, dpf, age,my_prediction,now))
        conn.commit()

        c.execute("SELECT * FROM kayitlar")
        rows = c.fetchall()
        old_records = []
        for row in rows:
            old_records.append(list(row))

        c.close()
        conn.close()
        
     



        return render_template('result.html', prediction=my_prediction,old_records=old_records)




if __name__ == '__main__':
	app.run(debug=True)