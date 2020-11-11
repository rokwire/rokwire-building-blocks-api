import json
import logging
import os
import random
import string
from time import gmtime
import requests
from controllers.auth import bp as auth_bp
from controllers.config import Config as cfg
from controllers.contribute import bp as contribute_bp
from db import init_app
from flask import g, Flask, jsonify, redirect, url_for, render_template, request, make_response, render_template_string
from flask import session as login_session
from flask_dance.contrib.github import make_github_blueprint, github

debug = cfg.DEBUG

log = logging.getLogger('werkzeug')
log.disabled = True

logging.Formatter.converter = gmtime
log_format = '%(asctime)-15s.%(msecs)03dZ %(levelname)-7s [%(threadName)-10s] : %(name)s - %(message)s'

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
static_dir = os.path.join(os.path.abspath('webapps'), 'static')
app = Flask(__name__, instance_relative_config=True, static_url_path=staticpath, static_folder=static_dir,
            template_folder=template_dir)
app.config.from_object(cfg)

init_app(app)
app.register_blueprint(contribute_bp)

app.config["GITHUB_CLIENT_ID"] = os.getenv("GITHUB_CLIENT_ID", "...")
app.config["GITHUB_CLIENT_SECRET"] = os.getenv("GITHUB_CLIENT_SECRET", "...")
app.secret_key = "supersekrit"
blueprint = make_github_blueprint(
    client_id=os.getenv("GITHUB_CLIENT_ID", "..."),
    client_secret=os.getenv("GITHUB_CLIENT_SECRET", "..."),
)
app.register_blueprint(blueprint, url_prefix="/login")


@app.route("/")
def index():
    if not github.authorized:
        return redirect(url_for("github.login"))
    resp = github.get("/user")
    assert resp.ok
    return render_template('contribute/home.html', user=resp.json()["login"])


# @app.route('/login')
# def login():
#     if session.get('user_id', None) is None:
#         return github.authorize()
#     else:
#         return 'Already logged in'

if __name__ == '__main__':
    app.run(port=5050, host=None, debug=True)
