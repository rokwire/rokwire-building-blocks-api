from flask import Flask
from flask_gzip import Gzip
from . import db
from . import logging_rest_service


def create_app():
    app = Flask(__name__, root_path='loggingservice/')
    app.url_map.strict_slashes = False
    app.register_blueprint(logging_rest_service.bp)
    app.config.from_pyfile('config.py', silent=True)

    Gzip(app, compress_level=app.config['GZIP_LEVEL'], minimum_size=app.config['GZIP_MIN_SIZE'])
    db.init_db(app)

    return app
