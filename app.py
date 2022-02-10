from flask import Flask, jsonify

from resources.pantrys import pantrys

import models

DEBUG = True
PORT = 8000

# Initialize an instance of the Flask class.
# This starts the website!
app = Flask(__name__)

app.register_blueprint(pantrys, url_prefix='/api/v1/pantrys')
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
