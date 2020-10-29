import json
import traceback

# from app import app
import requests
from controllers.config import Config
from flask import (
    abort, Blueprint, render_template, request, jsonify
)
from models.contribution_utilities import to_contribution

bp = Blueprint('contributions', __name__, url_prefix='/contributions')


@bp.route('/', methods=['GET', 'POST'])
def home():
    print("homepage.")
    if request.method == 'POST' and request.validate_on_submit():
        print("searching...")
        result = request.form.to_dict(flat=False)
        print(result)
        # search(result)
    return render_template('contributions/home.html')


@bp.route('/results', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        # result = request.form
        print("searching...")
        result = request.form.to_dict()
        print(result)
        query = result['search']
        search(query)
        return render_template("contributions/results.html", result=result)

@bp.route('/catalog/auth/callback', methods=['GET'])
def callback():
    if request.method == 'GET':
        print(request)
        code = None
        state = None
        try:
            code = request.args['code']
        except Exception:
            pass
        try:
            state = request.args['state']
        except Exception:
            pass
    print("test")

@bp.route('/create', methods=['GET', "POST"])
def create():
    if request.method == 'POST':
        result = request.form.to_dict(flat=False)
        # result = dict((key, request.form.getlist(key) if len(request.form.getlist(key)) > 1 else request.form.getlist(key)[0]) for key in request.form.keys())

        contribution = to_contribution(result)
        # print(contribution)
        json_contribution = json.dumps(contribution, indent=4)
        print(json_contribution)
        response,s = post(json_contribution)
        if response:
            return render_template('contributions/submitted.html')
        elif not response:
            return render_template('contributions/error.html', error_msg=s)
    return render_template('contributions/contributions.html')

@bp.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('contributions/submitted.html')

@bp.route('/submitted', methods=['GET', 'POST'])
def submitted():
    return render_template('contributions/submitted.html')


#

# @app.errorhandler(Exception)
# def handle_exception(e):
#     # pass through HTTP errors
#     if isinstance(e, HTTPException):
#         return e
#     # now you're handling non-HTTP exceptions only
#     return render_template("500_error.html", e=e), 500

@bp.route('/results')
def search_results(search):
    return render_template('results.html', results=results)


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
            print("post method fails".format(json_data))
            print("with error code:", result.status_code)
            return False, str("post method fails with error: ")+str(result.status_code)
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
            print("post method fails".format(input_data))
            print("with error code:", result.status_code)
            return False
        else:
            print("posted ok.".format(input_data))
            return True

    except Exception:
        # traceback.print_exc()
        return False
