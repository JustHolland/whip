from flask import Flask, jsonify

import models

DEBUG = True
PORT = 8000

# Initialize an instance of the Flask class.
# This starts the website!
app = Flask(__name__)


# The default URL ends in / ("my-website.com/").
@app.route('/')
def index():
    return 'Welcome to Whip.'

@app.route('/nested_json')
def get_nested_json():
    food_dict = {
        'item': 'chicken',
        'quanity': 2,

    }
    return jsonify(name="Justine", age=29, food=food_dict)



@app.route('/pantry/<username>') # When someone goes here...
def hello(username): # Do this.
    return f" {username}'s Pantry"

# Run the app when the program starts!
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)
