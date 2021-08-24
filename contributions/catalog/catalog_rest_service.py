import logging
import os
from time import gmtime

from flask import Flask, redirect, url_for, render_template, request, session
from requests_oauthlib import OAuth2Session
from controllers.auth import login_required
from controllers.config import Config as cfg
from controllers.contribute import bp as contribute_bp
from db import init_app

debug = cfg.DEBUG

log = logging.getLogger('werkzeug')
log.disabled = False

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

from jinja2 import Template, environment
from jinja2.filters import FILTERS, environmentfilter


@environmentfilter
def do_reverse_by_word(environment, value, attribute=None):
    """
    custom max calculation logic
    """
    if attribute:
        return [list(reversed(i.get(attribute).split())) for i in value]

    return list(reversed(value.split()))

@app.template_filter('filter_nested_dict')
def filter_nested_dict(dict, item_list):
    try:
        for item in item_list:
            dict = dict[item]
    except:
        return ''

    return dict

environment.DEFAULT_FILTERS['filter_nested_dict'] = filter_nested_dict

@app.route("/", methods=["GET"])
def index():
    return render_template('contribute/home.html')


@app.route("/login")
def login():
    """Step 1: Get the user identify for authentication.
    """
    # print("Step 1: User Authorization")
    github = OAuth2Session(cfg.GITHUB_CLIENT_ID)
    authorization_url, state = github.authorization_url(cfg.AUTHORIZATION_BASE_URL)

    # State is used to prevent CSRF.
    session['oauth_state'] = state

    return redirect(authorization_url)


# Step 2: User authorization, this happens on the provider.
# "http://localhost:5050/contributions/catalog/auth/callback"
@app.route("/contributions/catalog/auth/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.
    """
    # print("Step 3: Retrieving an access token")
    github = OAuth2Session(cfg.GITHUB_CLIENT_ID, state=session['oauth_state'])
    token = github.fetch_token(cfg.TOKEN_URL, client_secret=cfg.GITHUB_CLIENT_SECRET,
                               authorization_response=request.url)
    session['oauth_token'] = token

    return redirect(url_for('.profile'))

@app.route("/contribute/profile", methods=["GET"])
def profile():
    """Fetching a protected resource using an OAuth 2 token.
    Parsing the username to the seesion dict, to the templates to display.
    """
    # print("Fetching a protected resource using an OAuth 2 token")
    github = OAuth2Session(cfg.GITHUB_CLIENT_ID, token=session['oauth_token'])
    resp = github.get('https://api.github.com/user')
    session["username"] = resp.json()["login"]
    session['name'] = resp.json()["name"]

    return render_template('contribute/home.html', user=session["name"], token=session['oauth_token']['access_token'])


if __name__ == '__main__':
    app.run(port=5050, host=None, debug=True)
