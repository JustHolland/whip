import models

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, current_user, logout_user # this will be used to do the session

users = Blueprint('users', 'users')

@users.route('/', methods=['GET'])
def test_user_resource():
    return "user resource works"

@users.route('/register', methods=['POST'])
def register():
    payload = request.get_json()

    # since emails are case insensitive in the world
    payload['email'] = payload['email'].lower()
    # might as well do the same with username
    payload['username'] = payload['username'].lower()
    print(payload)

    # see if the user exists
    try:
        # .get is nice -- http://docs.peewee-orm.com/en/latest/peewee/querying.html#selecting-a-single-record
        models.User.get(models.User.email == payload['email'])
        # this will throw an error ("models.DoesNotExist exception")
        return jsonify(
            data={},
            messsage="A user with that email already exists",
            status=401
        ), 401
    except models.DoesNotExist: # except is like a catch in JS
        pw_hash = generate_password_hash(payload['password'])

        created_user = models.User.create(
            username=payload['username'],
            email=payload['email'],
            password=pw_hash
        )

        login_user(created_user)

        created_user_dict = model_to_dict(created_user)

        print(created_user_dict)

        print(type(created_user_dict['password']))
        created_user_dict.pop('password')

        return jsonify(
            data=created_user_dict,
            message=f"Successfully registered user {created_user_dict['email']}",
            status=201
        ), 201

@users.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    payload['email'] = payload['email'].lower()
    payload['username'] = payload['username'].lower()

    try:
        user = models.User.get(models.User.email == payload['email'])

        user_dict = model_to_dict(user)
        password_is_good = check_password_hash(user_dict['password'], payload['password'])

        if(password_is_good):
            # LOG THE USER IN!! using flask_login
            login_user(user) # in express we did this manually by setting stuff in session
            print(f"{current_user.username} is current_user.username in POST login")

            return jsonify(
                data=user_dict,
                message=f"Successfully logged in {user_dict['email']}",
                status=200
            ), 200
        else:
            print("email is no good")
            return jsonify(
                data={},
                message="Email or password is incorrect", # let's be vague
                status=401
            ), 401

    except models.DoesNotExist:
        print('email not found')
        return jsonify(
            data={},
            message="Email or password is incorrect", # let's be vague
            status=401
        ), 401

@users.route('/logged_in_user', methods=['GET'])
def get_logged_in_user():
    print(current_user)
    print(type(current_user))  # <class 'werkzeug.local.LocalProxy'> # google it if you're interested
    print(f"{current_user.username} is current_user.username in GET logged_in_user")
    user_dict = model_to_dict(current_user)
    user_dict.pop('password')

    return jsonify(data=user_dict), 200

@users.route('/logout', methods=['GET'])
def logout():
      # following the logout here: https://flask-login.readthedocs.io/en/latest/#login-example
      logout_user()
      return jsonify(
        data={},
        message="Successfully logged out.",
        status=200
      ), 200
