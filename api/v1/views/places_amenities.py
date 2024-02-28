#!/usr/bin/python3
"""
Route for handling amenity objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from os import environ
from models.amenity import Amenity


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def get_amenity_by_place(place_id):
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    if environ.get('HBNB_TYPE_STORAGE') == "db":
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get("Amenity", amenity_id).to_dict() for
                     amenity_id in place.amenity_ids]
    return jsonify(amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    place = storage.get("Place", place_id)
    if not place:
        abort(404, 'place not found')
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404, "amenity not found")

    if environ.get('HBNB_TYPE_STORAGE') == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"], strict_slashes=False)
def create_amenity(place_id, amenity_id):
    place = storage.get("Place", place_id)
    if not place:
        abort(404, 'invalid place')
    data = request.get_json()
    if not data:
        abort(400, 'missing json data')
    data["place_id"] = place_id
    data["amenity_id"] = amenity_id

    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201
