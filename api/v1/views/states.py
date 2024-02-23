#!/usr/bin/python3
"""
views module for the state routes
and api requests
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.state import State

@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_all_states():
    return jsonify([state.to_dict() for state in storage.all("State").values()])

@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    state = storage.get("State", state_id)
    return jsonify(state.to_dict()) if state else abort(404)

@app_views.route("/states/<state_id>", methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    state = storage.get("State", state_id)
    storage.delete(state) if state else abort(404)
    storage.save()
    return jsonify({}), 200

@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    state_data = request.get_json()
    if not state_data or "name" not in state_data:
        abort(400, 'Invalid JSON or missing name')
    state = State(**state_data)
    state.save()
    return jsonify(state.to_dict()), 201

@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    state_data = request.get_json()
    if not state_data:
        abort(400, 'Invalid JSON')
    for key, value in state_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
