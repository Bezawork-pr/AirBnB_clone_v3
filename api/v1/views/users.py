#!/usr/bin/python3
"""Create a new view for State objects that
handles all default RESTFul API actions for users"""
from api.v1.views import app_views
from flask import Flask, request, abort, jsonify, make_response
from models import storage
from models.user import User


@app_views.route('/users',
                 methods=['GET'], strict_slashes=False)
def users():
    """Get all users"""
    users_list = []
    users = storage.all(User)
    if users is None:
        abort(404)
    for keys, values in users.items():
        users_list.append(values.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Get user with user id"""
    user = storage.get(User, str(user_id))
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users',
                 methods=['POST'], strict_slashes=False)
def post_user():
    """Create new user"""
    post_request = request.get_json()
    if post_request is None:
        abort(400, "Not a JSON")
    if 'name' in post_request:
        user = User(**post_request)
        storage.new(user)
        storage.save()
        return make_response(jsonify(user.to_dict()), 201)
    else:
        abort(400, "Missing name")


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    user = storage.get(User, str(user_id))
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    put_request = request.get_json()
    if not put_request:
        abort(400, "Not a JSON")
    user = storage.get(User, str(user_id))
    if user is None:
        abort(404)
    put_list = ['id', 'created_at', 'updated_at']
    for keys, values in put_request.items():
        if keys not in put_list:
            setattr(user, keys, values)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
