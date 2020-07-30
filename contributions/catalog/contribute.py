import json
import traceback

import requests
from flask import (
    Blueprint, render_template, request, current_app
)

from .config import Config
from .db import get_db
from .utilities.contribution_utilities import to_contribution

bp = Blueprint('contribute', __name__, url_prefix='/contribute')


@bp.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        pass

    return render_template('contribute/home.html')


@bp.route('/create', methods=['GET', "POST"])
def create():
    if request.method == 'POST':
        result = request.form.to_dict(flat=False)
        # result = dict((key, request.form.getlist(key) if len(request.form.getlist(key)) > 1 else request.form.getlist(key)[0]) for key in request.form.keys())
        contribution = to_contribution(result)
        json_contribution = json.dumps(contribution, indent = 4)
        print(json_contribution)
        post(json_contribution)
    return render_template('contribute/contribute.html', )


@bp.route('/submitted', methods=['GET', 'POST'])
def submitted():
    return render_template('contribute/submitted.html')


# post a json_data in a http request
def post(json_data):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + Config.AUTHENTICATION_TOKEN
    }

    try:
        # Setting up post request
        result = requests.post(Config.CONTRIBUTION_BUILDING_BLOCK_URL, headers=headers,
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