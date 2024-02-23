#!/usr/bin/python3
from flask import Flask
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_appcontext(arg=None):
    """
    Method For handling closing of each session
    """
    storage.close()

@app.errorhandler(404)
def page_not_found(e):
    error_json = {
            "error": "Not found"
            }
    return error_json, 404

if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
