from flask import Flask
from . import AppConfigDatabase
from . import AppConfigRestService


def create_app():
    # create and configure the app
    app = Flask(__name__, root_path='app/configs')
    app.url_map.strict_slashes = False
    app.register_blueprint(AppConfigRestService.bp)
    app.config.from_pyfile('configs.py', silent=True)
    # Connect to database
    AppConfigDatabase.init_app(app)

    return app
