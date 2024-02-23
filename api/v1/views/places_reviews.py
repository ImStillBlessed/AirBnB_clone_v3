#!/usr/bin/python3
"""
Route for handling Review objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.review import Review

@app_views.route("/places/<place_id>/reviews", methods=["GET"], strict_slashes=False)
def get_review_by_place(place_id):
    place = storage.get("Place", place_id)
    return jsonify([review.to_dict() for review in place.review]) if place else abort(404)
@app_views.route("/reviews/<review_id>", methods=['GET'], strict_slashes=False)

def get_review(review_id):
    review = storage.get("Review", review_id)
    return jsonify(review.to_dict()) if review else abort(404)

@app_views.route("/reviews/<review_id>", methods=["DELETE"], strict_slashes=False)
def delete_review(review_id):
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200

@app_views.route("/places/<place_id>/reviews", methods=["POST"], strict_slashes=False)
def create_review(place_id):
    place = storage.get("Place", place_id)
    data = request.get_json()
    if not (place and data and "user_id" in data and "name" in data and storage.get("User", data["user_id"])):
        abort(400, 'Invalid JSON or missing user_id/name')
    data["place_id"] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201

@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    review = storage.get("review", review_id)
    data = request.get_json()
    if not (review and data):
        abort(404 if not review else 400, 'Invalid JSON')
    for key, value in data.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
