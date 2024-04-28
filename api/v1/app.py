#!/usr/bin/python3
""" app """

from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
import os
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(exception):
    """" Teardown Database"""
    storage.close()


@app.errorhandler(404)
def not_found(exception):
    """ Not Found 404 """
    out = jsonify(
        {
            "error": "Not found"
        }
    )
    out.status_code = 404
    return out


if __name__ == "__main__":
    HOST = os.getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=HOST, port=PORT, threaded=True)
