#!/usr/bin/python3
"""
create a variable app, instance of Flask
register the blueprint app_views to your Flask instance app
"""
from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardownapp(exc):
    """Tear down current session"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """Error handle 404 page not found"""
    return jsonify(error="Not found")


if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')
    host = HBNB_API_HOST if HBNB_API_HOST else '0.0.0.0'
    port = HBNB_API_PORT if HBNB_API_PORT else 5000
    app.run(host=host, port=port, threaded=True)
