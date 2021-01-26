import logging
import os
from time import gmtime

from dotenv import dotenv_values
from flask import Flask, redirect, url_for, render_template, request, session
from flask_cors import CORS
from requests_oauthlib import OAuth2Session

from controllers.contribute import bp as contribute_bp
from db import init_app

debug = os.getenv("DEBUG", "True")

log = logging.getLogger('werkzeug')
log.disabled = True

logging.Formatter.converter = gmtime
log_format = '%(asctime)-15s.%(msecs)03dZ %(levelname)-7s [%(threadName)-10s] : %(name)s - %(message)s'

if debug:
    logging.basicConfig(datefmt='%Y-%m-%dT%H:%M:%S', format=log_format, level=logging.DEBUG)
else:
    logging.basicConfig(datefmt='%Y-%m-%dT%H:%M:%S', format=log_format, level=logging.INFO)

URL_PREFIX = os.getenv("URL_PREFIX", "")
if URL_PREFIX:
    staticpath = URL_PREFIX + '/static'
else:
    staticpath = '/static'

template_dir = os.path.join(os.path.abspath('webapps'), 'templates')
static_dir = os.path.join(os.path.abspath('webapps'), 'static')
app = Flask(__name__, instance_relative_config=True, static_url_path=staticpath, static_folder=static_dir,
            template_folder=template_dir)

init_app(app)
# CORS(app, resources={r"/localhost:5050/*": {"origins": "*"}}, supports_credentials=True)
app.register_blueprint(contribute_bp)

# read configs variable from .env file
config = dotenv_values(".env")
app.config.update(config)

client_id = config["CLIENT_ID"]
client_secret = config["CLIENT_SECRET"]
authorization_base_url = config["authorization_base_url"]
token_url = config["token_url"]
contribution_url = config["CONTRIBUTION_BUILDING_BLOCK_URL"]


@app.route("/")
def index():
    """Step 1: Get the user identify for authentication.
    """
    print("Step 1: User Authorization")
    github = OAuth2Session(client_id)
    authorization_url, state = github.authorization_url(authorization_base_url)
    # print(authorization_url, state)
    # State is used to prevent CSRF.
    session['oauth_state'] = state
    # print(session)
    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider.
# "http://localhost:5050/contributions/catalog/auth/callback"
@app.route("/contributions/catalog/auth/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.
    """
    # print("Step 3: Retrieving an access token")
    github = OAuth2Session(client_id, state=session['oauth_state'])
    token = github.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.url)

    # print(token)
    session['oauth_token'] = token
    return redirect(url_for('.profile'))

@app.route("/profile", methods=["GET"])
def profile():
    """Fetching a protected resource using an OAuth 2 token.
    Parsing the username to the seesion dict, to the templates to display.
    """
    # print("Fetching a protected resource using an OAuth 2 token")
    github = OAuth2Session(client_id, token=session['oauth_token'])
    resp = github.get('https://api.github.com/user')
    # print(resp.json())
    session["username"] = resp.json()["login"]
    session['name'] = resp.json()["name"]
    return render_template('contribute/home.html', user=session["name"])


if __name__ == '__main__':
    app.run(port=5050, host=None, debug=True)