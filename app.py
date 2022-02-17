

from flask import Flask, jsonify


from resources.pantrys import pantrys 
from resources.users import users

import models


from flask_cors import CORS


from flask_login import LoginManager

import os


from dotenv import load_dotenv

load_dotenv()

DEBUG=True
PORT=8000


app = Flask(__name__) # instantiating the Flask class to create an app


app.secret_key = os.environ.get("APP_SECRET")


login_manager = LoginManager()

login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    try:
        print("loading the following user")
        user = models.User.get_by_id(user_id)

        return user
    except models.DoesNotExist:
        return None


CORS(pantrys, origins=['http://localhost:3000'], supports_credentials=True)
CORS(users, origins=['http://localhost:3000'], supports_credentials=True)


app.register_blueprint(pantrys, url_prefix='/api/v1/pantrys')
app.register_blueprint(users, url_prefix='/api/v1/users')

@app.route('/') # @ symbol here means this is a decorator
def hello():
    return 'Hello, world!'


@app.route('/test')
def get_list():
    return ['hello', 'hi', 'hey']

@app.route('/test_json')
def get_json():

    return jsonify(['hello', 'hi', 'hey'])

@app.route('/say_hello/<username>')
def say_hello(username): # this function takes the URL parameter as an arg
    return f"Hello {username}"



if __name__ == '__main__':

    models.initialize()
    app.run(debug=DEBUG, port=PORT)
