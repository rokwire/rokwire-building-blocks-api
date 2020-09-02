import os
import requests
import logging
from flask import Flask, render_template, request, Blueprint
from controllers.auth import bp as auth_bp
from controllers.config import Config as cfg
from controllers.contribute import bp as contribute_bp
from db import init_app
from time import gmtime


debug = cfg.DEBUG

log = logging.getLogger('werkzeug')
log.disabled = True

logging.Formatter.converter = gmtime
log_format ='%(asctime)-15s.%(msecs)03dZ %(levelname)-7s [%(threadName)-10s] : %(name)s - %(message)s'

if debug:
    logging.basicConfig(datefmt='%Y-%m-%dT%H:%M:%S', format=log_format, level=logging.DEBUG)
else:
    logging.basicConfig(datefmt='%Y-%m-%dT%H:%M:%S', format=log_format, level=logging.INFO)
if cfg and cfg.URL_PREFIX:
    prefix = cfg.URL_PREFIX
    staticpath = prefix + '/static'
else:
    staticpath = '/static'

template_dir = os.path.join(os.path.abspath('webapps'), 'templates')
app = Flask(__name__, instance_relative_config=True, static_url_path=staticpath, template_folder=template_dir)
# app = Flask(__name__, instance_relative_config=True, static_url_path=staticpath)
app.config.from_object(cfg)

init_app(app)
app.register_blueprint(auth_bp)
app.register_blueprint(contribute_bp)

@app.route('/')
def hello():
    return render_template('contribute/home.html')


if __name__ == '__main__':
    app.run(port=5050, host=None, debug=True)

