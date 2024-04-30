#!/usr/bin/python3
"""Contains the index view for the API"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {
    "amenities": Amenity,
    "cities": City,
    "places": Place,
    "reviews": Review,
    "states": State,
    "users": User
}


@app_views.route("/status")
def status():
    """Status of the API"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """count objects by type"""
    elements = {}

    for key, value in classes.items():
        elements[key] = storage.count(value)
    return jsonify(elements)
