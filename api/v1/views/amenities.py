#!/usr/bin/python3
"""
Route for handling Amenity objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"],
                 strict_slashes=False)
def get_all_amenities():
    return jsonify([amenity.to_dict() for amenity in
                    storage.all("Amenity").values()])


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity(amenity_id):
    amenity = storage.get("Amenity", amenity_id)
    return jsonify(amenity.to_dict()) if amenity else abort(404)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    amenity = storage.get("Amenity", amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    amenity_data = request.get_json()
    if not amenity_data or "name" not in amenity_data:
        abort(400, 'Invalid JSON or missing name')
    amenity = Amenity(**amenity_data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    amenity = storage.get("Amenity", amenity_id)
    if amenity:
        amenity_data = request.get_json()
        if not amenity_data:
            abort(400, 'Invalid JSON')
        for key, value in amenity_data.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
    abort(404)
