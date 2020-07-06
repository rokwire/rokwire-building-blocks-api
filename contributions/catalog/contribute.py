import functools
import pymongo
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db
from .config import Config
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
        print(contribution)
        db = get_db()
        mycol = db[Config.DB_COLLECTION]
        x = mycol.insert_one(contribution)
    return render_template('contribute/contribute.html',)


@bp.route('/submitted', methods=['GET', 'POST'])
def submitted():
    return render_template('contribute/submitted.html')















