#!/usr/bin/python3
""" index """

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def api_status():
    """api status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
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
    return jsonify(classes)
