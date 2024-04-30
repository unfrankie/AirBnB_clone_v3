#!/usr/bin/python3
""" index """
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_status():
    """api status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def obj_count():
    """Endpoint that retrieves the number of each objects by type"""
    classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
    }
    cls = {}
    for key, val in classes.items():
        cls[key] = storage.count(val)
    return jsonify(cls)
