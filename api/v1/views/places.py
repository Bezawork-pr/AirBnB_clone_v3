#!/usr/bin/python3
"""Create a new view for State objects that
handles all default RESTFul API actions for place"""
from api.v1.views import app_views
from flask import Flask, request, abort, jsonify, make_response
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def place(city_id):
    """handles default RESTFul API actions for GET"""
    city = storage.get(City, city_id)
    place_list = []
    if city is None:
        abort(404)
    place = storage.all(Place)
    for keys, values in place.items():
        if values.city_id == city_id:
            place_list.append(values.to_dict())
    return jsonify(place_list)


@app_views.route('places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Get place with place id"""
    place = storage.get(Place, str(place_id))
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """Create new Place"""
    post_request = request.get_json()
    if post_request is None:
        abort(400, "Not a JSON")
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if 'name' not in post_request:
        abort(400, "Missing name")
    if 'user_id' not in post_request:
        abort(400, "Missing user_id")
    post_request['city_id'] = city_id
    place = Place(**post_request)
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Delete place with place id"""
    place = storage.get(Place, str(place_id))
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """Update place using place id"""
    put_request = request.get_json()
    if not put_request:
        abort(400, "Not a JSON")
    place = storage.get(Place, str(place_id))
    if place is None:
        abort(404)
    put_list = ['id', 'created_at', 'updated_at']
    for keys, values in put_request.items():
        if keys not in put_list:
            setattr(place, keys, values)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
