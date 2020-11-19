import json
import logging
import os
import random
import string
from urllib.parse import urlencode
from requests_oauthlib import OAuth2Session
from uuid import uuid4
import os
from time import gmtime
import requests
from controllers.auth import bp as auth_bp
from controllers.config import Config as cfg
from controllers.contribute import bp as contribute_bp
from db import init_app
from flask import g, Flask, jsonify, redirect, url_for, render_template, request, make_response, render_template_string, \
    session
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



# client_id = os.getenv("GITHUB_CLIENT_ID", "...")
# client_secret = os.getenv("GITHUB_CLIENT_SECRET", "...")
# authorization_base_url = 'https://github.com/login/oauth/authorize'
# token_url = 'https://github.com/login/oauth/access_token'



# This information is obtained upon registration of a new GitHub OAuth
# application here: https://github.com/settings/applications/new
client_id = "73675deda5732fe96f62"
client_secret = "842faa650c2d23aa31573e824a38c32cf1b4fb11"
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'


API_BASE = "http://localhost:5050"
CLIENT_ID = "deee5ee488009a044d7c"
CLIENT_SECRET = "53c40f67771236250bb7a9ebebf76b893d1b7063"
# REDIRECT_URI = "http://localhost:5050/contributions/catalog/auth/callback"
REDIRECT_URI = "http://localhost:5050"

@app.route("/")
def demo():
    """Step 1: User Authorization.

    Redirect the user/resource owner to the OAuth provider (i.e. Github)
    using an URL with a few key OAuth parameters.
    """
    github = OAuth2Session(client_id)
    authorization_url, state = github.authorization_url(authorization_base_url)

    # State is used to prevent CSRF, keep this for later.
    session['oauth_state'] = state
    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider.

@app.route("/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.

    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    github = OAuth2Session(client_id, state=session['oauth_state'])
    token = github.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.url)

    # At this point you can fetch protected resources but lets save
    # the token and show how this is done from a persisted token
    # in /profile.
    session['oauth_token'] = token

    return redirect(url_for('.profile'))


@app.route("/profile", methods=["GET"])
def profile():
    """Fetching a protected resource using an OAuth 2 token.
    """
    github = OAuth2Session(client_id, token=session['oauth_token'])
    return jsonify(github.get('https://api.github.com/user').json())

# """
# using Flask-dance
# """
# @app.route("/")
# def index():
#     if not github.authorized:
#         return redirect(url_for("github.login"))
#     resp = github.get("/user")
#     assert resp.ok
#     g.user = resp.json()["login"]
#     return render_template('contribute/home.html', user=resp.json()["login"])


if __name__ == '__main__':
    app.run(port=5050, host=None, debug=True)