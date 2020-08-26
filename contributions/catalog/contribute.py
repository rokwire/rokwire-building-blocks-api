import json
import traceback

import requests
from flask import (
    Blueprint, render_template, request
)

from .config import Config
from .utilities.contribution_utilities import to_contribution

bp = Blueprint('contribute', __name__, url_prefix='/contribute')


@bp.route('/', methods=['GET', 'POST'])
def home():
    print("homepage.")
    if request.method == 'POST' and request.validate_on_submit():
        print("searching...")
        result = request.form.to_dict(flat=False)
        print(result)
        # search(result)
    return render_template('contribute/home.html')


@bp.route('/results',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      # result = request.form
      print("searching...")
      result = request.form.to_dict()
      print(result)
      query = result['search']
      search(query)
      return render_template("contribute/results.html",result = result)


@bp.route('/create', methods=['GET', "POST"])
def create():
    if request.method == 'POST':
        result = request.form.to_dict(flat=False)
        # result = dict((key, request.form.getlist(key) if len(request.form.getlist(key)) > 1 else request.form.getlist(key)[0]) for key in request.form.keys())

        contribution = to_contribution(result)
        # print(contribution)
        json_contribution = json.dumps(contribution, indent=4)
        print(json_contribution)
        post(json_contribution)
    return render_template('contribute/contribute.html', )


@bp.route('/submitted', methods=['GET', 'POST'])
def submitted():
    return render_template('contribute/submitted.html')

#

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
            return False
        else:
            print("posted ok.".format(json_data))
            return True

    except Exception:
        traceback.print_exc()
        return False


# post a json_data in a http request
def search(input_data):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + Config.AUTHENTICATION_TOKEN
    }

    try:
        # Setting up post request
        if not input_data or len(input_data) == 0:
            result = requests.get(Config.CONTRIBUTION_BUILDING_BLOCK_URL+"/",
                               headers=headers)
        else:
            result = requests.get(Config.CONTRIBUTION_BUILDING_BLOCK_URL+"/"+str(input_data),
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