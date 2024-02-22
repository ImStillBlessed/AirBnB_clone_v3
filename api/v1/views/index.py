from api.v1.views import app_views
from flask import render_template

@app_views.route("/status", strict_slashes=False)
def status():
    output = {
        "status": "OK"
        }
    return output