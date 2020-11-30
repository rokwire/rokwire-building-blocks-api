import logging
from requests_oauthlib import OAuth2Session
import logging
import os
from time import gmtime

from flask import Flask, redirect, url_for, render_template, request, session
from requests_oauthlib import OAuth2Session

from controllers.config import Config as cfg
from controllers.contribute import bp as contribute_bp
from db import init_app

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

client_id = os.getenv("CLIENT_ID", "NO ID")
client_secret = os.getenv("CLIENT_SECRET", "NO SECRET")
authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'


@app.route("/")
def demo():
    """Step 1: User Authorization.
    """
    # print("Step 1: User Authorization")
    github = OAuth2Session(client_id)
    authorization_url, state = github.authorization_url(authorization_base_url)

    # State is used to prevent CSRF.
    session['oauth_state'] = state
    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider.

@app.route("/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.
    """
    # print("Step 3: Retrieving an access token")
    github = OAuth2Session(client_id, state=session['oauth_state'])
    token = github.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.url)

    session['oauth_token'] = token
    return redirect(url_for('.profile'))

@app.route("/profile", methods=["GET"])
def profile():
    """Fetching a protected resource using an OAuth 2 token.
    and parse the user name to the templates to display.
    """
    print("Fetching a protected resource using an OAuth 2 token")
    github = OAuth2Session(client_id, token=session['oauth_token'])
    resp = github.get('https://api.github.com/user')
    return render_template('contribute/home.html', user=resp.json()["login"])


# """
# using Flask-dance for auth
# """
# app.config["GITHUB_CLIENT_ID"] = os.getenv("GITHUB_CLIENT_ID", "...")
# app.config["GITHUB_CLIENT_SECRET"] = os.getenv("GITHUB_CLIENT_SECRET", "...")
# app.secret_key = "supersekrit"
# blueprint = make_github_blueprint(
#     client_id=os.getenv("GITHUB_CLIENT_ID", "..."),
#     client_secret=os.getenv("GITHUB_CLIENT_SECRET", "..."),
# )
# app.register_blueprint(blueprint, url_prefix="/login")
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