#!/usr/bin/python3
"""Create a new view for State objects that
handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import Flask, request, abort, jsonify, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def state():
    """handles default RESTFul API actions for GET"""
    state = storage.all(State)
    return jsonify([elem.to_dict() for elem in state.values()])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Get state with state id"""
    state = storage.get(State, str(state_id))
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Create new state"""
    post_request = request.get_json()
    if post_request is None:
        abort(400, "Not a JSON")
    elif 'name' in post_request:
        state = State(**post_request)
        storage.new(state)
        storage.save()
        return make_response(jsonify(state.to_dict()), 201)
    else:
        abort(400, "Missing name")


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete state with state id"""
    state = storage.get(State, str(state_id))
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """Update state using state id"""
    put_request = request.get_json()
    if not put_request:
        abort(400, "Not a JSON")
    state = storage.get(State, str(state_id))
    if state is None:
        abort(404)
    put_list = ['id', 'created_at', 'updated_at']
    for keys, values in put_request.items():
        if keys not in put_list:
            setattr(state, keys, values)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
