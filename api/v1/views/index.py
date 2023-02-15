#!/usr/bin/python3
"""
Index file
"""
from api.v1.views import app_views
from flask import jsonify, Flask
from models import storage


app = Flask(__name__)


@app_views.route('/status', strict_slashes=False)
def status():
    """Return status ok"""
    return jsonify(status="OK")


@app_views.route('/stats', strict_slashes=False)
def count():
    """Count using count method in storage"""
    obj = {}
    obj['amenities'] = storage.count('Amenity')
    obj['cities'] = storage.count('City')
    obj['places'] = storage.count('Place')
    obj['reviews'] = storage.count('Review')
    obj['states'] = storage.count('State')
    obj['users'] = storage.count('User')
    return jsonify(obj)
