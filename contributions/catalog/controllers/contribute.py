import json
import traceback

import requests
import functools
from flask import (
    Blueprint, render_template, request, session, redirect, url_for
)
from requests_oauthlib import OAuth2Session
from .auth import login_required
from controllers.config import Config as cfg
from models.contribution_utilities import to_contribution
from utils import jsonutil

bp = Blueprint('contribute', __name__, url_prefix='/contribute')


@bp.route('/', methods=['GET', 'POST'])
def home():
    print("homepage.")
    if request.method == 'POST' and request.validate_on_submit():
        result = request.form.to_dict(flat=False)
    if "name" in session:
        return render_template('contribute/home.html', user=session["name"], token=session['oauth_token']['access_token'])
    else:
        return render_template('contribute/home.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Step 1: Get the user identify for authentication.
    """
    # print("Step 1: User Authorization")
    github = OAuth2Session(cfg.GITHUB_CLIENT_ID)
    authorization_url, state = github.authorization_url(cfg.AUTHORIZATION_BASE_URL)

    # State is used to prevent CSRF.
    session['oauth_state'] = state
    # print(session)
    return redirect(authorization_url)


@bp.route('/logout')
def logout():
    session.clear()
    return render_template('contribute/home.html')


@bp.route('/results', methods=['POST', 'GET'])
@login_required
def result():
    if request.method == 'POST':
        # result = request.form
        result = request.form.to_dict()
        query = result['search']
        search(query)
        return render_template("contribute/results.html", user=session["name"],  token=session['oauth_token']['access_token'], result=result)




@bp.route('/create', methods=['GET', "POST"])
@login_required
def create():
    if request.method == 'POST':
        result = request.form.to_dict(flat=False)
        # result = dict((key, request.form.getlist(key) if len(request.form.getlist(key)) > 1 else request.form.getlist(key)[0]) for key in request.form.keys())

        contribution = to_contribution(result)
        # add contributionAdmins to the json_contiubtion
        contribution = jsonutil.add_contribution_admins(contribution)
        json_contribution = json.dumps(contribution, indent=4)
        response, s = post(json_contribution)
        if response:
            if response:
                if "name" in session:
                    return render_template('contribute/submitted.html', user=session["name"],  token=session['oauth_token']['access_token'])
                else:
                    return render_template('contribute/submitted.html')
            elif not response:
                if "name" in session:
                    return render_template('contribute/error.html', user=session["name"],  token=session['oauth_token']['access_token'], error_msg=s)
                else:
                    return render_template('contribute/error.html', error_msg=s)
    return render_template('contribute/contribute.html', user=session["name"],  token=session['oauth_token']['access_token'])


@bp.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('contribute/submitted.html', user=session["name"],  token=session['oauth_token']['access_token'])


@bp.route('/submitted', methods=['GET', 'POST'])
@login_required
def submitted():
    return render_template('contribute/submitted.html', user=session["name"],  token=session['oauth_token']['access_token'])


@bp.route('/results')
@login_required
def search_results(search):
    return render_template('results.html', results=results, user=session["name"],  token=session['oauth_token']['access_token'])


# post a json_data in a http request
def post(json_data):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + session['oauth_token']['access_token']
    }
    try:
        # Setting up post request
        result = requests.post(cfg.CONTRIBUTION_BUILDING_BLOCK_URL,
                               headers=headers,
                               data=json_data)

        if result.status_code != 200:
            print("post method fails".format(json_data))
            print("with error code:", result.status_code)
            return False, str("post method fails with error: ") + str(result.status_code)
        else:
            print("posted ok.".format(json_data))
            return True, str("post success!")

    except Exception:
        traceback.print_exc()
        var = traceback.format_exc()
        return False, var


# post a json_data in a http request
def search(input_data):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + cfg.AUTHENTICATION_TOKEN
    }

    try:
        # Setting up post request
        if not input_data or len(input_data) == 0:
            result = requests.get(cfg.CONTRIBUTION_BUILDING_BLOCK_URL + "/",
                                  headers=headers)
        else:
            result = requests.get(cfg.CONTRIBUTION_BUILDING_BLOCK_URL + "/" + str(input_data),
                                  headers=headers)

        if result.status_code != 200:
            print("post method fails".format(input_data))
            print("with error code:", result.status_code)
            return False
        else:
            print("posted ok.".format(input_data))
            return True

    except Exception:
        # traceback.print_exc()
        return False
