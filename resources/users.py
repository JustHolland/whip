import models

from flask import Blueprint, request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
from flask_login import login_user, current_user, logout_user


users= Blueprint('users', 'users')

@users.route('/', methods=['GET'])
def test_user_resource():
    return "user  works"


@users.route('/register', methods=['POST'])
def register():
    payload = request.get_json()
    payload['email'] = payload['email'].lower()
    payload['username'] = payload['username'].lower()
    print(payload)

    try:
        models.User.get(models.User.email == payload['email'])

        return jsonify(
            data={},
            messsage="A user with that email already exists",
            status=401
        ), 401


    except models.DoesNotExist:
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
            message="Successfully registered user",
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
            login_user(user)
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
                message="Email or password is incorrect",
                status=401
            ), 401

    except models.DoesNotExist:

        print('email not found')

        return jsonify(
            data={},
            message="Email or password is incorrect",
            status=401
        ), 401

@users.route('/logged_in_user', methods=['GET'])
def get_logged_in_user():
    print(current_user)
    print(type(current_user))
    print(f"{current_user.username} is current_user.username in GET logged_in_user")
    user_dict = model_to_dict(current_user)
    user_dict.pop('password')

    return jsonify(data=user_dict), 200

@users.route('/logout', methods=['GET'])
def logout():
      logout_user()
      return jsonify(
        data={},
        message="Successfully logged out.",
        status=200
      ), 200
