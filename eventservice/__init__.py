from flask import Flask
from . import db
from . import event_rest_service


def create_app():
    # create and configure the app
    app = Flask(__name__, root_path='eventservice/')
    app.url_map.strict_slashes = False
    app.register_blueprint(event_rest_service.bp)
    app.config.from_pyfile('config.py', silent=True)
    # Connect to database
    db.init_db(app)

    return app
