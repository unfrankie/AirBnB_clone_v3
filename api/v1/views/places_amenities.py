#!/usr/bin/python3
""" places/amenities """
from flask import jsonify, abort
from os import getenv
from api.v1.views import app_views, storage


@app_views.route('/places/<place_id>/amenities', methods=['GET', 'POST'],
                 strict_slashes=False)
def place_amenities(place_id):
    """ place_amenity defenition """
    place = storage.get("Place", place_id)
    amenities_l = []
    if not place:
        abort(404)
    if request.method == 'GET':
        for obj in amenities_l.amenities:
            amenities_l.append(obj.to_dict())
        return jsonify(amenities_l)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"],
                 strict_slashes=False)
def amenity_place(place_id, amenity_id):
    """ Post """
    place = storage.get("Place", str(place_id))
    amenity = storage.get("Amenity", str(amenity_id))
    if request.method == 'POST':
        for obj in place.amenities:
            if str(obj.id) == amenity_id:
                result = obj
                break
        if not amenity or not place:
            abort(404)
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
        place.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
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
