#!/usr/bin/python3
""" Amenities """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage, Amenity

@app_views.route('/amenities', methods=['GET', 'POST'])
def amenities():
    """ amenities defenition """
    if request.method == 'GET':
        amenities = [amenity.to_dict() for amenity in storage.all("Amenity").values()]
        return jsonify(amenities)
    if request.method == 'POST':
        if not request.json:
            abort(400, "Not a JSON")
        if 'name' not in request.json:
            abort(400, "Missing name")
        amenity = Amenity(**request.json)
        amenity.save()
        return jsonify(amenity.to_dict()), 201

@app_views.route('/amenities/<amenity_id>', methods=['GET', 'PUT', 'DELETE'])
def amenity(amenity_id):
    """ amenities definition """
    amenity = storage.get("Amenity", amenity_id)
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
        amenity.delete()
        storage.save()
        return jsonify({})
