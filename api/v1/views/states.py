from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State

@app_views.route("/states", methods=['GET', 'POST'])
def for_states():
    if request.method == 'GET':
        states = storage.all('State')
        return [state.to_dict() for state in states]
    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a JSON"}), 400
        if 'name' not in data:
            return jsonify({"error": "Missing name"}), 400
        new_state = State(**data)
        new_state.save()
        return new_state.to_dict(), 201
    
@app_views.route('/states/<state_id>', methods=['GET', 'PUT','DELETE'])
def for_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        return jsonify({"error": "State not found"}), 404
    
    if request.method == 'GET':
        return state.to_dict()
    
    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a JSON"}), 400
        for key, value in data.items():
            if key not in ['id', 'created_at', 'uptated_at']:
                setattr(state, key, value)
        state.save()
        return state.to_dict(), 200
    
    elif request.method == 'DELETE':
        state.delete()
        return jsonify({}), 200
    
