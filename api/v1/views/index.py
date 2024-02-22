from api.v1.views import app_views
from models import storage

@app_views.route("/status", strict_slashes=False)
def status():
    output = {
        "status": "OK"
        }
    return output

@app_views.route("/api/v1/stats", strict_slashes=False)
def 
