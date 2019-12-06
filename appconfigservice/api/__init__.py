from .utils import db
from .controllers import app

"""
def create_app(test_config=None):
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    # to load the test config
    if test_config is None:
        # to load the instance config if exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.update(test_config)

    app.register_blueprint(rest_service.bp)

    # Connect to database
    db.init_db(app)

    return app
"""

