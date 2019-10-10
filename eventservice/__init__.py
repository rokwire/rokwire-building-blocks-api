from flask import Flask
from flask_gzip import Gzip
from . import db
from . import event_rest_service


def create_app():
    # create and configure the app
    app = Flask(__name__, root_path='eventservice/')
    app.url_map.strict_slashes = False
    app.register_blueprint(event_rest_service.bp)
    app.config.from_pyfile('config.py', silent=True)

    Gzip(app, compress_level=app.config['GZIP_LEVEL'], minimum_size=app.config['GZIP_MIN_SIZE'])
    # Connect to database
    db.init_db(app)

    return app
