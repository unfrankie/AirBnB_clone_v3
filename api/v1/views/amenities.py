#!/usr/bin/python3
""" Amenities """
from flask import jsonify, request, abort
from api.v1.views import app_views, storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def amenities():
    """ amenities defenition """
    if request.method == 'GET':
        amenities = []
        amenity = storage.all("Amenity")
        for obj in amenity.values():
            amenities.append(obj.to_dict())
        return jsonify(amenities)
    if request.method == 'POST':
        if not request.json:
            abort(400, "Not a JSON")
        if 'name' not in request.json:
            abort(400, "Missing name")
        amenity = Amenity(**request.json)
        amenity.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def amenity(amenity_id):
    """ amenities definition """
    amenity = storage.get("Amenity", str(amenity_id))
    if not amenity:
        abort(404)
    if request.method == 'GET':
        return jsonify(amenity.to_dict())
    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        for key, value in request.json.items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict())
    if request.method == 'DELETE':
        amenity = storage.get("Amenity", str(amenity_id))
        storage.delete(amenity)
        storage.save()
        return jsonify({})
