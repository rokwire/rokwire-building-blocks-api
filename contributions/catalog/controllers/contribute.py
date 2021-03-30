import json
import traceback

# from app import app
import requests
from flask import (
    Blueprint, render_template, request, session, redirect, url_for
)
from requests_oauthlib import OAuth2Session

from controllers.config import Config as cfg
from controllers.config import Config
from models.contribution_utilities import to_contribution

bp = Blueprint('contribute', __name__, url_prefix='/contribute')

@bp.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST' and request.validate_on_submit():
        # print("searching...")
        result = request.form.to_dict(flat=False)
    if "name" in session:
        return render_template('contribute/home.html', user=session["name"])
    else:
        return render_template('contribute/home.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Step 1: Get the user identify for authentication.
    """
    # print("Step 1: User Authorization")
    github = OAuth2Session(cfg.CLIENT_ID)
    authorization_url, state = github.authorization_url(cfg.AUTHORIZATION_BASE_URL)

    # State is used to prevent CSRF.
    session['oauth_state'] = state
    return redirect(authorization_url)

@bp.route('/logout')
def logout():
    session.clear()
    return render_template('contribute/home.html')

@bp.route('/results', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form.to_dict()
        query = result['search']
        search(query)
        return render_template("contribute/results.html", user=session["name"], result=result)


@bp.route('/create', methods=['GET', "POST"])
def create():
    if request.method == 'POST':
        result = request.form.to_dict(flat=False)
        # result = dict((key, request.form.getlist(key) if len(request.form.getlist(key)) > 1 else request.form.getlist(key)[0]) for key in request.form.keys())

        contribution = to_contribution(result)
        json_contribution = json.dumps(contribution, indent=4)
        response, s = post(json_contribution)
        if response:
            if "name" in session:
                return render_template('contribute/submitted.html', user=session["name"])
            else:
                return render_template('contribute/submitted.html')
        elif not response:
            if "name" in session:
                return render_template('contribute/error.html', user=session["name"], error_msg=s)
            else:
                return render_template('contribute/error.html', error_msg=s)

    return render_template('contribute/contribute.html', user=session["name"])

@bp.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('contribute/submitted.html', user=session["name"])

@bp.route('/submitted', methods=['GET', 'POST'])
def submitted():
    return render_template('contribute/submitted.html', user=session["name"], )


@bp.route('/results')
def search_results(search):
    return render_template('results.html', results=results, user=session["name"], )

# post a json_data in a http request
def post(json_data):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + Config.AUTHENTICATION_TOKEN
    }
    try:
        # Setting up post request
        result = requests.post(Config.CONTRIBUTION_BUILDING_BLOCK_URL,
                               headers=headers,
                               data=json_data)

        if result.status_code != 200:
            return False, str("post method fails with error: ")+str(result.status_code)
        else:
            return True, str("post success!")

    except Exception:
        traceback.print_exc()
        var = traceback.format_exc()
        return False, var


# post a json_data in a http request
def search(input_data):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + Config.AUTHENTICATION_TOKEN
    }

    try:
        # Setting up post request
        if not input_data or len(input_data) == 0:
            result = requests.get(Config.CONTRIBUTION_BUILDING_BLOCK_URL + "/",
                                  headers=headers)
        else:
            result = requests.get(Config.CONTRIBUTION_BUILDING_BLOCK_URL + "/" + str(input_data),
                                  headers=headers)

        if result.status_code != 200:
            return False
        else:
            return True

    except Exception:
        # traceback.print_exc()
        return False
