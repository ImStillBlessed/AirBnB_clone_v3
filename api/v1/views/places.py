#!/usr/bin/python3
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.place import Place
from models.city import City
from models.user import User

@app_views.route("/cities/<city_id>/places", methods=["GET"], strict_slashes=False)
def get_places_by_city(city_id):
    city = storage.get("City", city_id)
    return jsonify([place.to_dict() for place in city.places]) if city else abort(404)

@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    place = storage.get("Place", place_id)
    return jsonify(place.to_dict()) if place else abort(404)

@app_views.route("/places/<place_id>", methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200

@app_views.route("/cities/<city_id>/places", methods=["POST"], strict_slashes=False)
def create_place(city_id):
    city = storage.get("City", city_id)
    data = request.get_json()
    if not (city and data and "user_id" in data and "name" in data and storage.get("User", data["user_id"])):
        abort(400, 'Invalid JSON or missing user_id/name')
    data["city_id"] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201

@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    place = storage.get("Place", place_id)
    data = request.get_json()
    if not (place and data):
        abort(404 if not place else 400, 'Invalid JSON')
    for key, value in data.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
