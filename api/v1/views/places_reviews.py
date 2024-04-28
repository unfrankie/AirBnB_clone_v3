#!/usr/bin/python3
""" reviews """
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def reviews(place_id):
    """ reviews defenition """
    reviews_l = []
    place = storage.get("Place", str(place_id))
    if place is None:
        abort(404)
    if request.method == 'GET':
        for obj in place.reviews:
            reviews_l.append(obj.to_dict())
        return jsonify(reviews_l)
    if request.method == 'POST':
        json = request.get_json(silent=True)
        if json is None:
            abort(400, 'Not a JSON')
        if not storage.get("Place", place_id):
            abort(404)
        if not storage.get("User", json["user_id"]):
            abort(404)
        if "user_id" not in json:
            abort(400, 'Missing user_id')
        if "text" not in json:
            abort(400, 'Missing text')
        json["place_id"] = place_id
        new = Review(**json)
        new.save()
        return jsonify(new.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def review(review_id):
    """ reviews id """
    review = storage.get("Review", str(review_id))
    if not review:
        abort(404)
    if request.method == 'GET':
        return jsonify(review.to_dict())
    if request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        for key, value in request.json.items():
            if key not in [
                'id', 'user_id', 'place_id',
                'created_at', 'updated_at'
            ]:
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict())
    if request.method == 'DELETE':
        if fetched_obj is None:
            abort(404)
        storage.delete(review)
        storage.save()
        return jsonify({})
