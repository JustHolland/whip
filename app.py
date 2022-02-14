from flask import Flask, jsonify

from resources.pantrys import pantrys
from resources.users import users

import models
from flask_cors import CORS
from flask_login import LoginManager


DEBUG = True
PORT = 8000


app = Flask(__name__)
app.secret_key = "ALGERNON"
login_manager = LoginManager()
login_manager.init_app(app)



CORS(pantrys, origins=['http://localhost:3000'], supports_credentials=True)
CORS(users, origins=['http://localhost:3000'], supports_credentials=True)


app.register_blueprint(pantrys, url_prefix='/api/v1/pantrys')
app.register_blueprint(users, url_prefix='/api/v1/users')
# The default URL ends in / ("my-website.com/").
@app.route('/')
def index():
    return 'Welcome to Whip.'

@app.route('/nested_json')
def get_nested_json():
    pantry_dict = {
        'item': 'chicken',
        'quantity': 2,
        'category': 'meat_fridge',
    }
    return jsonify(name="Justine", age=29, pantry=pantry_dict)



@app.route('/pantry/<username>') # When someone goes here...
def hello(username): # Do this.
    return f" {username}'s Pantry"

# Run the app when the program starts!
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
