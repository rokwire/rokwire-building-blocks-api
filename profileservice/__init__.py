from flask import Flask
from . import profile_rest_service
# from . import db

def create_app():
    # create and configure the app
    app = Flask(__name__, root_path='profileservice/')
    app.url_map.strict_slashes = False
    # app.register_blueprint(profile_rest_service.bp)
    app.config.from_pyfile('configs.py', silent=True)
    # Connect to database
    # db.init_app(app)

    return app