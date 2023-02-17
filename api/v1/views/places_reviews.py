#!/usr/bin/python3
"""Create a new view for State objects that
handles all default RESTFul API actions for Review"""
from api.v1.views import app_views
from flask import Flask, request, abort, jsonify, make_response
from models import storage
from models.place import Place
from models.city import City
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def place_review(place_id):
    """handles default RESTFul API actions for GET"""
    place = storage.get(Place, place_id)
    review_list = []
    if place is None:
        abort(404)
    review = storage.all(Review)
    for keys, values in review.items():
        if values.place_id == place_id:
            review_list.append(values.to_dict())
    return jsonify(review_list)


@app_views.route('reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Get review with review id"""
    review = storage.get(Review, str(review_id))
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """Create new Review"""
    post_request = request.get_json()
    if post_request is None:
        abort(400, "Not a JSON")
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if 'user_id' not in post_request:
        abort(400, "Missing user_id")
    if 'text' not in post_request:
        abort(400, "Missing text")
    post_request['place_id'] = place_id
    review = Review(**post_request)
    storage.new(review)
    storage.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete review with review id"""
    review = storage.get(Review, str(review_id))
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """Update review using review id"""
    put_request = request.get_json()
    if not put_request:
        abort(400, "Not a JSON")
    review = storage.get(Review, str(review_id))
    if review is None:
        abort(404)
    put_list = ['id', 'created_at', 'updated_at', 'place_id', 'user_id']
    for keys, values in put_request.items():
        if keys not in put_list:
            setattr(review, keys, values)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
