import os

import flask
from flask_cors import CORS

def create_app(test_config=None):
    app = flask.Flask(__name__, instance_relative_config=True)
    cors = CORS(app, resources={r"/queue/*": {"origins": "*"}})

    @app.route('/queue/v1/events')
    def hello():
        with open('mock-backend/mock-events.json', "r") as f:
            data =  f.read()
            return data

    return app
