#  Copyright 2021 Board of Trustees of the University of Illinois.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import logging
import json
import os
import utils.requestutil as requestutil
import utils.jsonutil as jsonutil

from time import gmtime
from jinja2 import environment
from flask import Flask, redirect, url_for, render_template, request, session
from requests_oauthlib import OAuth2Session

from controllers.config import Config as cfg
from controllers.contribute import bp as contribute_bp
from db import init_app
from werkzeug.middleware.proxy_fix import ProxyFix

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

# TODO: Experimental fix for running behind the load balancer. Revisit to verify that this fix matches the actual deployment environment. Ref: https://werkzeug.palletsprojects.com/en/2.1.x/middleware/proxy_fix/
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)

init_app(app)
app.register_blueprint(contribute_bp)


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
    show_sel = request.args.get('show')
    is_logged_in = False
    cap_json = []
    tal_json = []
    user = None

    if 'GIT_TAG' in os.environ:
        git_tag=os.environ['GIT_TAG']
    else:
        git_tag=''
    if 'GIT_SHA' in os.environ:
        git_sha=os.environ['GIT_SHA']
    else:
        git_sha=''

    try:
        # create error to see if the user is logged in or now
        # TODO this should be changed to better way
        if (session["name"] == ""):
            is_logged_in = True
        else:
            is_logged_in = True
        user=session["name"]
        token=session['oauth_token']['access_token']
    except:
        is_logged_in = False

    if (is_logged_in):
        # query with auth
        headers = requestutil.get_header_using_session(session)
        result = requestutil.request_contributions(headers)
        if show_sel == "capability":
            # create the json for only capability
            cap_json = jsonutil.create_capability_json_from_contribution_json(result.json())
        elif show_sel == "talent":
            # create the json for only talent
            tal_json = jsonutil.create_talent_json_from_contribution_json(result.json())
        else:
            # create the json for only capability and talent
            cap_json = jsonutil.create_capability_json_from_contribution_json(result.json())
            tal_json = jsonutil.create_talent_json_from_contribution_json(result.json())
    else:
        # query only published ones
        show_err_message = False
        headers = requestutil.get_header_using_api_key()
        result = requestutil.request_contributions(headers)

        if result.status_code != 200:
            msg = {
                "ERROR": "There is a problem getting contributions list. Maybe API Key is not correct."
            }
            msg_json = jsonutil.create_log_json("Contribution", "SEARCH", msg)
            logging.info("Contribution SEARCH " + json.dumps(msg_json))
            show_err_message = True

        if show_sel == "capability":
            # create the json for only capability
            cap_json = jsonutil.create_capability_json_from_contribution_json(result.json())
        elif show_sel == "talent":
            # create the json for only talent
            tal_json = jsonutil.create_talent_json_from_contribution_json(result.json())
        else:
            # create the json for only capability and talent
            cap_json = jsonutil.create_capability_json_from_contribution_json(result.json())
            tal_json = jsonutil.create_talent_json_from_contribution_json(result.json())

        # show connection error message to main page
        if show_err_message:
            err_msg = "ERROR: There is a problem getting contributions list. Please try again later."
            return render_template('contribute/error.html', error_msg=err_msg)
        else:
            return render_template('contribute/home.html', git_tag=git_tag, git_sha=git_sha,
                                   cap_json=cap_json, tal_json=tal_json, show_sel=show_sel, user=user)

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
@app.route("/catalog/auth/callback", methods=["GET"])
def callback():
    """ Step 3: Retrieving an access token.
    """
    # print("Step 3: Retrieving an access token")
    if 'oauth_state' in session:
        github = OAuth2Session(cfg.GITHUB_CLIENT_ID, state=session['oauth_state'])
    else:
        github = OAuth2Session(cfg.GITHUB_CLIENT_ID, state=None)
    token = github.fetch_token(cfg.TOKEN_URL, client_secret=cfg.GITHUB_CLIENT_SECRET,
                               authorization_response=request.url)
    session['oauth_token'] = token

    # Retrieve basic user info
    github = OAuth2Session(cfg.GITHUB_CLIENT_ID, token=session['oauth_token'])
    resp = github.get(cfg.USER_INFO_URL)
    session["username"] = resp.json()["login"]
    session['name'] = resp.json()["name"]

    return redirect(url_for('contribute.home'))

if __name__ == '__main__':
    app.run(port=cfg.CATALOG_PORT, host=None, debug=True)
