from flask import Flask
from appconfig import db
from appconfig import rest_service

def create_app(test_config=None):
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)
        
    app.register_blueprint(rest_service.bp)
  
    # Connect to database
    db.init_app(app)

    return app
    
if __name__ == "__main__":
    myapp = create_app()
    myapp.run(debug=True)