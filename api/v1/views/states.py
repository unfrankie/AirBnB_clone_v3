#!/usr/bin/python3
""" State """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage, State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def states():
    """ state defenition """
    states = []
    if request.method == 'GET':
        state_objs = storage.all(State).values()
        states = [obj.to_dict() for obj in state_objs]
        return jsonify(states)
    elif request.method == 'POST':
        json_data = request.get_json(silent=True)
        if not json_data:
            return jsonify({"error": "Not a JSON"}), 400
        if 'name' not in json_data:
            return jsonify({"error": "Missing name"}), 400
        new_state = State(**json_data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def state(state_id):
    """ State id """
    state = storage.get("State", str(state_id))
    if not state:
        abort(404)
    if request.method == 'GET':
        return jsonify(state.to_dict())
    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        for key, value in request.json.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict())
    if request.method == 'DELETE':
        if state is None:
            abort(404)
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
