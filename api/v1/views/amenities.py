#!/usr/bin/python3
"""Create a new view for State objects that
handles all default RESTFul API actions for Amenity"""
from api.v1.views import app_views
from flask import Flask, request, abort, jsonify, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities',
                 methods=['GET'], strict_slashes=False)
def amenity():
    """Get all amenities"""
    amenities_list = []
    amenities = storage.all(Amenity)
    if amenities is None:
        abort(404)
    for keys, values in amenities.items():
        amenities_list.append(values.to_dict())
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Get Amenity with Amenity Id"""
    amenity = storage.get(Amenity, str(amenity_id))
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities',
                 methods=['POST'], strict_slashes=False)
def post_amenity():
    post_request = request.get_json()
    if post_request is None:
        abort(400, "Not a JSON")
    if 'name' in post_request:
        amenity = Amenity(**post_request)
        storage.new(amenity)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 201)
    else:
        abort(400, "Missing name")


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    amenity = storage.get(Amenity, str(amenity_id))
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    put_request = request.get_json()
    if not put_request:
        abort(400, "Not a JSON")
    amenity = storage.get(Amenity, str(amenity_id))
    if amenity is None:
        abort(404)
    put_list = ['id', 'created_at', 'updated_at']
    for keys, values in put_request.items():
        if keys not in put_list:
            setattr(amenity, keys, values)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
