#!/usr/bin/python3
""" Users """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage, User


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def users():
    """ Users definition """
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


@app_views.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def user(user_id):
    """ Users ID """
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        for key, value in request.json.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict())
    if request.method == 'DELETE':
        user.delete()
        storage.save()
        return jsonify({})
