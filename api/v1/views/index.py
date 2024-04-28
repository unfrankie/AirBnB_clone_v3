#!/usr/bin/python3
""" index """

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_status():
    """api status"""
    out = jsonify({"status": "OK"})
    out.status_code = 200
    return out


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def obj_count():
    """Endpoint that retrieves the number of each objects by type"""
    classes = {
        "Amenity": storage.count(Amenity),
        "City": storage.count(City),
        "Place": storage.count(Place),
        "Review": storage.count(Review),
        "State": storage.count(State),
        "User": storage.count(User)
    }
    out = jsonify(classes)
    out.status_code = 200
    return out
