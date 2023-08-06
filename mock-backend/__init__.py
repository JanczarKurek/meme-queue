import os

import flask
from flask_cors import CORS

def create_app(test_config=None):
    app = flask.Flask(__name__, instance_relative_config=True)
    cors = CORS(app, resources={r"*": {"origins": "*"}})

    @app.route('/queue/v1/events')
    def events():
        with open('mock-backend/mock-events.json', "r") as f:
            data =  f.read()
            return data
    
    @app.route('/queue/v1/currentEvents')
    def current_events():
        with open('mock-backend/mock-current-events.json', "r") as f:
            data =  f.read()
            return data
        

    @app.route('/media/images/<path:path>')
    def send_image(path):
        return flask.send_from_directory('media/images', path)

    return app
