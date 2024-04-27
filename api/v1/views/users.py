#!/usr/bin/python3
""" Users """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage, User


@app_views.route('/users', methods=['GET', 'POST'])
def users():
    """ Users defenition """
    if request.method == 'GET':
        users = [user.to_dict() for user in storage.all("User").values()]
        return jsonify(users)
    if request.method == 'POST':
        if not request.json:
            abort(400, "Not a JSON")
        if 'email' not in request.json:
            abort(400, "Missing email")
        if 'password' not in request.json:
            abort(400, "Missing password")
        user = User(**request.json)
        user.save()
        return jsonify(user.to_dict()), 201

@app_views.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def user(user_id):
    """ users id """
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        for key, value in request.json.items():
            if key != 'id' and key != 'email' and key != 'created_at' and key != 'updated_at':
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict())
    if request.method == 'DELETE':
        user.delete()
        storage.save()
        return jsonify({})
