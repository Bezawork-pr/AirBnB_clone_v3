#!/usr/bin/python3
"""Create a new view for State objects that
handles all default RESTFul API actions for city"""
from api.v1.views import app_views
from flask import Flask, request, abort, jsonify, make_response
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def city(state_id):
    """Get cities with the state id provided"""
    state = storage.get(State, str(state_id))
    city_list = []
    if state is None:
        abort(404)
    city = storage.all(City)
    for keys, values in city.items():
        if values.state_id == state_id:
            city_list.append(values.to_dict())
    return jsonify(city_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Get city with city id"""
    city = storage.get(City, str(city_id))
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """Create new city"""
    post_request = request.get_json()
    if post_request is None:
        abort(400, "Not a JSON")
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if 'name' in post_request:
        post_request['state_id'] = state_id
        city = City(**post_request)
        storage.new(city)
        storage.save()
        return make_response(jsonify(city.to_dict()), 201)
    else:
        abort(400, "Missing name")


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Delete city with city id"""
    city = storage.get(City, str(city_id))
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Update city using city id"""
    put_request = request.get_json()
    if not put_request:
        abort(400, "Not a JSON")
    city = storage.get(City, str(city_id))
    if city is None:
        abort(404)
    put_list = ['id', 'created_at', 'updated_at']
    for keys, values in put_request.items():
        if keys not in put_list:
            setattr(city, keys, values)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
