#!/usr/bin/python3
""" Cities """
from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models import storage, City, State


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def cities_by_state(state_id):
    """ Cities defenition """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    if request.method == 'GET':
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)
    if request.method == 'POST':
        if not request.json:
            abort(400, "Not a JSON")
        if 'name' not in request.json:
            abort(400, "Missing name")
        city = City(**request.json)
        city.state_id = state_id
        city.save()
        return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'PUT', 'DELETE'])
def city(city_id):
    """ City ID """
    city = storage.get("City", city_id)
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
        city.delete()
        storage.save()
        return jsonify({})
