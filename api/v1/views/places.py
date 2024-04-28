#!/usr/bin/python3
""" Places """
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def places(city_id):
    """ Places defenition """
    places = []
    json = request.get_json(silent=True)
    if request.method == 'GET':
        city = storage.get("City", str(city_id))
        if not city:
            abort(404)
        for obj in city.places:
            places.append(obj.to_dict())
        return jsonify(places)
    if request.method == 'POST':
        if json is None:
            abort(400, 'Not a JSON')
        if not storage.get("User", json["user_id"]):
            abort(404)
        if not storage.get("City", city_id):
            abort(404)
        if "user_id" not in json:
            abort(400, 'Missing user_id')
        if "name" not in json:
            abort(400, 'Missing name')


@app_views.route('/places/<place_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def place(place_id):
    """ places id """
    json = request.get_json(silent=True)
    place = storage.get("Place", str(place_id))
    if json is None:
        abort(400, 'Not a JSON')
    if not place:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())
    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        for key, value in request.json.items():
            if key not in {'id', 'user_id', 'city_id',
                           'created_at', 'updated_at'}:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict())
    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({})


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def search_places():
    """
    Search
    """
    if request.get_json() is None:
        abort(400, description="Not a JSON")
    search_params = request.get_json()
    states = search_params.get('states', [])
    cities = search_params.get('cities', [])
    amenities = search_params.get('amenities', [])
    places = []
    if not states and not cities and not amenities:
        places = storage.all(Place).values()
    else:
        if states:
            for state_id in states:
                state = storage.get(State, state_id)
                if state:
                    for city in state.cities:
                        places.extend(city.places)
        if cities:
            for city_id in cities:
                city = storage.get(City, city_id)
                if city:
                    places.extend(city.places)
        if amenities:
            amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
            places = [
                place for place in places
                if all(am in place.amenities for am in amenities_obj)
            ]
    places_dicts = [place.to_dict() for place in places]
    for place_dict in places_dicts:
        place_dict.pop('amenities', None)
    return jsonify(places_dicts)
