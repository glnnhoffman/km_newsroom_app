from flask import Flask, render_template, request
import mysql.connector
from mysql.connector import errorcode
import pandas as pd
import sqlalchemy
import os
from dotenv import load_dotenv

#Load credentials
load_dotenv('cred.env')
rmi_db = os.getenv('DBASE_PWD')
rmi_ip = os.getenv('DBASE_IP')

# connect to database
config = {
  'host': rmi_ip,
  'user':'rmiadmin',
  'password': rmi_db,
  'database':'rmi_km_news',
  'client_flags': [mysql.connector.ClientFlag.SSL],
  'ssl_ca': 'C:/Users/ghoffman/OneDrive - RMI/01. Projects/DigiCertGlobalRootCA.crt.pem'
}
# Construct connection string
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/createProfile')
def createProfile():
    return 'Create Profile'

@app.route('/resources')
def resources():
    cursor.execute("SELECT title, pubDate, source, url_full_txt from portal_live where url_full_txt IS NOT NULL and pubDate > (curdate() - interval 1 week)")
    result = cursor.fetchall()
    return render_template('resources.html', data=result)

@app.route('/form')
def form():
    return render_template('form.html')
 
@app.route('/profile', methods = ['POST', 'GET'])
def profile():
    if request.method == 'GET':
        return "Login via the login Form"
     
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        frequency = request.form['frequency']
        cursor = conn.cursor()
        cursor.execute(''' INSERT INTO user_table VALUES(%s,%s,%s)''',(name,age,frequency))
        conn.commit()
        cursor.close()
        return f"Done!!"
 
@app.route('/search', methods=['GET'])
def search():
    if request.method == 'GET':
            name = request.form['name']
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user_table WHERE name = %s", (name))
            result = cursor.fetchall()
            cursor.close()
            return render_template('search.html', data=result)
    conn.commit()
    cursor.close()

if __name__ == '__main__':
    app.run(debug=True)


