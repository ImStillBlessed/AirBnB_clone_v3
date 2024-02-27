#!/usr/bin/python3
"""
Route for handling User objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_all_users():
    return jsonify([user.to_dict() for user in storage.all("User").values()])


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    user = storage.get("User", user_id)
    return jsonify(user.to_dict()) if user else abort(404)


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    user = storage.get("User", user_id)
    storage.delete(user) if user else abort(404)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    user_data = request.get_json()
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")
    user = User(**user_data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    user_data = request.get_json()
    if not user_data:
        abort(400, 'Invalid JSON')
    for key, value in user_data.items():
        if key not in ["id", "email", "password", "created_at", "updated_at"]:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
