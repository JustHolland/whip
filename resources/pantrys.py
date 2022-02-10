import models

from flask import Blueprint, request



pantrys= Blueprint('pantrys', 'pantrys')

@pantrys.route('/', methods=['GET'])
def pantrys_index():
    return "pantry is working"


@pantrys.route('/', methods=['POST'])
def create_pantry():
    payload = request.get_json()
    print(payload)
    new_pantry = models.Pantry.create(item=payload['item'], quantity=payload['quantity'], category=payload['category'])
    print(new_pantry)
    return "created a new item"
