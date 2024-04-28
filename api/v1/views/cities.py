#!/usr/bin/python3
""" Cities """
from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models import storage, City, State


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def cities_by_state(state_id):
    """ Cities defenition """
    cities = []
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    for obj in state_obj.cities:
        city_list.append(obj.to_json())
    return jsonify(city_list)
    if request.method == 'POST':
        if not request.json:
            abort(400, "Not a JSON")
        if 'name' not in request.json:
            abort(400, "Missing name")
        json_data = request.get_json()
        json_data['state_id'] = state_id
        new_city = City(**json_data)
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def city(city_id):
    """ City ID """
    city = storage.get('City', str(city_id))
    if not city:
        abort(404)
    if request.method == 'GET':
        return jsonify(city.to_dict())
    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        for key, value in request.json.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict())
    if request.method == 'DELETE':
        city = storage.get('City', str(city_id))
        storage.delete(city)
        storage.save()
        return jsonify({})
