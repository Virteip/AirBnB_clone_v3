#!/usr/bin/python3
"""Return a view of all amenities"""
from models.user import User
from models import storage
from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get():
    """ Retrieve amenities
    """
    user_list = []

    for key, user in storage.all("User").items():
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ Retrieves amenities by id
    """
    user_dict = storage.get("User", user_id)

    if user_dict:
        return jsonify(user_dict.to_dict())

    abort(404)


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete(user_id):
    """ Delete amenities
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        user = storage.get(User, user_id)
        storage.delete(user)
        storage.save()
        return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create():
    """ Create amenities
    """
    if not request.json:
        abort(400, "Not a JSON")

    if 'email' not in request.json:
        abort(400, "Missing email")

    if 'password' not in request.json:
        abort(400, "Missing password")

    user = models.user.User(**request.json)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update(user_id):
    """ Update amenities
    """
    user = storage.get('User', user_id)
    if not user:
        abort(404)

    json_content = request.get_json()

    if json_content is None:
        abort(400, 'Not a JSON')
    for key, value in json_content.items():
        if key is not 'id' and
        key is not 'created_ad' and
        key is not 'updated_at':
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
