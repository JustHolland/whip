import models

from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict

pantrys= Blueprint('pantrys', 'pantrys')

@pantrys.route('/', methods=['GET'])
def pantrys_index():
    result = models.Pantry.select()
    print('results of pantry')
    print(result)

    for pantry in result:
        print(pantry.__data__)

    pantry_dicts = [model_to_dict(pantry) for pantry in result]

    return jsonify({
        'data': pantry_dicts,
        'message': f"Successfullly found {len(pantry_dicts)} in the pantry",
        'status': 200
    }), 200


@pantrys.route('/', methods=['POST'])
def create_pantry():
    payload = request.get_json()
    print(payload)
    new_pantry = models.Pantry.create(item=payload['item'], quantity=payload['quantity'], category=payload['category'])
    print(new_pantry)
    print(new_pantry.__dict__)


    pantry_dict = model_to_dict(new_pantry)

    return jsonify(
    data= pantry_dict,
    message= 'Successfully created a new item in your pantry',
    status= 201
    ),201

@pantrys.route('/<id>', methods=['GET'])
def get_one_pantry(id):
    pantry = models.Pantry.get_by_id(id)
    print(pantry)

    return jsonify(
        data = model_to_dict(pantry),
        message = 'Success',
        status = 200
    ), 200


@pantrys.route('/<id>', methods=['PUT'])
def update_pantry(id):
    payload = request.get_json()
    models.Pantry.update(**payload).where(models.Pantry.id == id).execute()

    return jsonify(
        data=model_to_dict(models.Pantry.get_by_id(id)),
        message='resource updated successfully',
        status=200,
    ), 200


@pantrys.route('/<id>', methods=['DELETE'])
def delete_pantry(id):
    delete_query = models.Pantry.delete().where(models.Pantry.id == id)
    nums_of_rows_deleted = delete_query.execute()
    print(nums_of_rows_deleted)


    return jsonify(
        data={},
        message=f"Successfully deleted {nums_of_rows_deleted} item with id {id}",
        status=200
    ), 200
