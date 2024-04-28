#!/usr/bin/python3
""" State """
from api.v1.views import app_views, storage
from flask import jsonify, request, abort
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def states():
    """ state defenition """
    states = []
    state = storage.all("State")
    for obj in state.values():
        states.append(obj.to_json())
    return jsonify(states)
    json = request.get_json(silent=True)
    if json is None:
        abort(400, 'Not a JSON')
    if "name" not in json:
        abort(400, 'Missing name')
    new = State(**_json)
    new.save()
    out = jsonify(new_state.to_json())
    out.status_code = 201
    return out


@app_views.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE',
                 strict_slashes=False])
def state(state_id):
    """ State id """
    state = storage.get("State", str(state_id))
    if not state:
        abort(404)
    if request.method == 'GET':
        return jsonify(state.to_json())

    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        for key, value in request.json.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_json())

    if request.method == 'DELETE':
        state = storage.get("State", str(state_id))
        if state is None:
            abort(404)
        storage.delete(state)
        storage.save()
        return jsonify({})
