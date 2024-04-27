#!/usr/bin/python3
""" State """
from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models import storage, State


@app_views.route('/states', methods=['GET', 'POST'])
def states():
  """ state defenition """
  if request.method == 'GET':
    states = [state.to_dict() for state in storage.all("State").values()]
    return jsonify(states)
  if request.method == 'POST':
    if not request.json:
      abort(400, "Not a JSON")
    if 'name' not in request.json:
      abort(400, "Missing name")
    state = State(**request.json)
    state.save()
    return jsonify(state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE'])
def state(state_id):
    """ State id """
    state = storage.get("State", state_id)
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
        state.delete()
        storage.save()
        return jsonify({})
