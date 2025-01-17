#!/usr/bin/python3
"""
Route for handling Cities objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def get_cities_by_state(state_id):
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route("/cities/<city_id>", methods=["GET"],
                 strict_slashes=False)
def get_city(city_id):
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    city_data = request.get_json()
    if not city_data or "name" not in city_data:
        abort(400, 'Invalid JSON or missing name')
    city_data["state_id"] = state_id
    city = City(**city_data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"],
                 strict_slashes=False)
def update_city(city_id):
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    city_data = request.get_json()
    if not city_data:
        abort(400, 'Invalid JSON')
    for key, value in city_data.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
