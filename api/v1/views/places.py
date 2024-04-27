#!/usr/bin/python3
""" Places """
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.user import User


@app_views.route('/places', methods=['GET', 'POST'])
def places():
    """ Places defenition """
    if request.method == 'GET':
        places = [place.to_dict() for place in storage.all("Place").values()]
        return jsonify(places)
    if request.method == 'POST':
        if not request.json:
            abort(400, "Not a JSON")
        if 'user_id' not in request.json:
            abort(400, "Missing user_id")
        if 'name' not in request.json:
            abort(400, "Missing name")
        user_id = request.json['user_id']
        if not storage.get("User", user_id):
            abort(404)
        place = Place(**request.json)
        place.save()
        return jsonify(place.to_dict()), 201

@app_views.route('/places/<place_id>', methods=['GET', 'PUT', 'DELETE'])
def place(place_id):
    """ places id """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())
    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        for key, value in request.json.items():
            if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict())
    if request.method == 'DELETE':
        place.delete()
        storage.save()
        return jsonify({})

@app_views.route('/places_search', methods=['POST'])
def search_places():
    """ search places """
    search_params = request.get_json()
    if search_params is None:
        abort(400, 'Not a JSON')
    states = search_params.get('states', [])
    cities = search_params.get('cities', [])
    amenities = search_params.get('amenities', [])
    places = []
    if not states and not cities:
        places = storage.all(Place).values()
    else:
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    places.extend(city.places)
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                places.extend(city.places)
    if amenities:
        amenities_set = set(amenities)
        places = [place for place in places if amenities_set.issubset(set(place.amenities))]
    return jsonify([place.to_dict() for place in places])
