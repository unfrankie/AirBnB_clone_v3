#!/usr/bin/python3
""" reviews """
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage, Review, User, Place


@app_views.route('/reviews', methods=['GET', 'POST'])
def reviews():
    """ reviews defenition """
    if request.method == 'GET':
        reviews = [review.to_dict() for review in storage.all("Review").values()]
        return jsonify(reviews)
    if request.method == 'POST':
        if not request.json:
            abort(400, "Not a JSON")
        if 'user_id' not in request.json:
            abort(400, "Missing user_id")
        if 'place_id' not in request.json:
            abort(400, "Missing place_id")
        if 'text' not in request.json:
            abort(400, "Missing text")
        user_id = request.json['user_id']
        place_id = request.json['place_id']
        if not storage.get("User", user_id):
            abort(404)
        if not storage.get("Place", place_id):
            abort(404)
        review = Review(**request.json)
        review.save()
        return jsonify(review.to_dict()), 201

@app_views.route('/reviews/<review_id>', methods=['GET', 'PUT', 'DELETE'])
def review(review_id):
    """ reviews id """
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    if request.method == 'GET':
        return jsonify(review.to_dict())
    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        for key, value in request.json.items():
            if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict())
    if request.method == 'DELETE':
        review.delete()
        storage.save()
        return jsonify({})
