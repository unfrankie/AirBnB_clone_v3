#!/usr/bin/python3
""" places/amenities """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage, Place, Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET', 'POST'])
def place_amenities(place_id):
    """ place_amenity defenition """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    if request.method == 'GET':
        amenities = [amenity.to_dict() for amenity in place.amenities]
        return jsonify(amenities)
    if request.method == 'POST':
        if 'amenity_id' not in request.json:
            abort(400, "Missing amenity_id")
        amenity_id = request.json['amenity_id']
        amenity = storage.get("Amenity", amenity_id)
        if not amenity:
            abort(404)
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
        place.save()
        return jsonify(amenity.to_dict()), 201

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """ place_amenity ID """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    if amenity not in place.amenities:
        abort(404)
    place.amenities.remove(amenity)
    place.save()
    return jsonify({}), 200
