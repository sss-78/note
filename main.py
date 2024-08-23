import anthropic
import os
from flask import Flask, render_template, request
import json
import psycopg2
import schemas
from flask_pydantic import validate
from sqlalchemy.orm import sessionmaker, declarative_base
import model
import database
import utils


app = Flask(__name__, template_folder='templates')

# Claude testing page
@app.route('/output/')
def hello_world():
    #value = call()
    value = 'Currently in testing'
    return value

# Login Page
@app.route('/')
def home():
    return render_template('login.html')

# Sign-up stuff
@app.route('/signup')
def signup():
    return render_template('signup.html')

# Creating a new note page
@app.route('/new_note')
def note():
    return render_template('new_note.html')

# Info displayed after signing-up
@app.route('/sign-up-info', methods = ['POST'])
@validate(on_success_status=201)
def get_sign_in_info(form: schemas.RequestFormDataModel):
    username, email, password = form.username, form.email, form.password
    hashed_password = utils.hash(password)
    database.add_user(username, email, hashed_password)
    value = schemas.UserResponseModel(username=username, email=email).dict()
    
    return_value = ''
    for fields in value:
        return_value += fields + ' ' + value[fields] + '\n'
    
    return render_template("note-response.html", message_value=f"{return_value}"), {"Refresh": "2; url=/"}

@app.route('/api/sign-up-info', methods = ['POST'])
@validate(on_success_status=201)
def get_sign_in_info_api(body: schemas.RequestBodyDataModel):
    username, email, password = body.username, body.email, body.password   
    hashed_password = utils.hash(password)
    database.add_user(username, email, hashed_password)
    return schemas.UserResponseModel(username=username, email=email)

# Displying all users
@app.route('/api/users')
def get_users_api():
    try:
        conn = database.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM users;'
        cursor.execute(query)

        users = cursor.fetchall()

        users = [schemas.UserResponseModel(username=user[1], email=user[2]).model_dump() for user in users]

        cursor.close()
        conn.close()
        return {"users" : users}
    except Exception as e:
        print(e)

    return {"users" : "something wrong happened"}

@app.route('/login', methods = ['POST'])
@validate(on_success_status=200)
def validate_login(form: schemas.RequestFormLoginDataModel):
    username, password = form.username, form.password
    message = ""

    try:
        conn = database.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM users where username=%s;'
        cursor.execute(query, [username])

        user = cursor.fetchall()

        if not user:
            message = "User not found"
        else:
            validated = utils.validate_password(password, user[0][3])
            print(validated)
            message = "Incorrect Login Info" if not validated else f"You are logged in as {user[0][1]}"
            
        cursor.close()
        conn.close()
    except Exception as e:
        print(e)
    
    file = "user.html" if message[0:3] == "You" else "error.html"
    return render_template(file, message_value=message) 


if __name__ == '__main__':
    # connect_to_database()
    # database.create_users_table()
    app.run(debug=True)