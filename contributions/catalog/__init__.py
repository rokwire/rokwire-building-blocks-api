import os

from flask import Flask, render_template

from .auth import bp as auth_bp
from .config import Config
from .contribute import bp as contribute_bp
from .db import init_app


def create_app(config_class=Config):
    if Config and Config.URL_PREFIX:
        prefix = Config.URL_PREFIX
        staticpath = prefix + '/static'
    else:
        staticpath = '/static'

    app = Flask(__name__, instance_relative_config=True, static_url_path=staticpath)
    app.config.from_object(Config)

    init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(contribute_bp)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def hello():
        # return 'Hello, World!'
        return render_template('contribute/home.html')

    return app
