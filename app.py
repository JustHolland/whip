
from flask import Flask, jsonify, after_this_request
from resources.pantrys import pantrys
from resources.users import users
import models

from flask_cors import CORS
from flask_login import LoginManager
import os


from dotenv import load_dotenv

load_dotenv()

DEBUG=True
PORT=os.environ.get("PORT")


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
##FE REACT APP

app.register_blueprint(pantrys, url_prefix='/api/v1/pantrys')
app.register_blueprint(users, url_prefix='/api/v1/users')


@app.before_request # use this decorator to cause a function to run before reqs
def before_request():

    """Connect to the db before each request"""
    print("you should see this before each request") # optional -- to illustrate that this code runs before each request -- similar to custom middleware in express.  you could also set it up for specific blueprints only.
    models.DATABASE.connect()

    @after_this_request # use this decorator to Executes a function after this request
    def after_request(response):
        """Close the db connetion after each request"""
        print("you should see this after each request") # optional -- to illustrate that this code runs after each request
        models.DATABASE.close()
        return response # go ahead and send response back to client
                      # (in our case this will be some JSON)

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

if os.environ.get('FLASK_ENV') != 'development':
  print('\non heroku!')
  models.initialize()

if __name__ == '__main__':
  models.initialize()
  app.run(debug=DEBUG, port=PORT)
