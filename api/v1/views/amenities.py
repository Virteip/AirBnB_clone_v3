#!/usr/bin/python3
"""Return a view of all amenities"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ Retrieve amenities
    """
    amenity_list = []

    for key, amenity in storage.all("Amenity").items():
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieves amenities by id
    """
    amenity_dict = storage.get("Amenity", amenity_id)

    if amenity:
        return jsonify(amenity_dict.to_dict())

    abort(404)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete(amenity_id):
    """ Delete amenities
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        amenity = storage.get(Amenity, amenity_id)
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create():
    """ Create amenities
    """
    if not request.json:
        abort(400, description="Not a JSON")

    if "name" not in request.get_json().keys():
        abort(400, description="Missing name")

    get_amenity = request.get_json()
    post_amenity = Amenity(**get_amenity)
    post_amenity.save()

    return jsonify(post_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update(amenity_id):
    """ Update amenities
    """
    if not request.json:
        abort(400, description="Not a JSON")

    get_amenity = storage.get("Amenity", amenity_id)

    if get_amenity is None:
        abort(404)

    data = request.get_json()

    for key, value in data.items():
        if key is not"id" or
        key is not "created_at" or
        key is not "updated_at":
            setattr(get_amenity, key, value)

    storage.save()
    return jsonify(get_amenity.to_dict()), 200
