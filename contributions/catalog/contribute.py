import functools
import pymongo
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db
from .config import Config

bp = Blueprint('contribute', __name__, url_prefix='/contribute')

@bp.route('/', methods=['GET', 'POST'])
def home():
    # if request.method == 'POST':
    #     title = request.form['title']
    #     body = request.form['body']
    #     error = None
    #
    #     if not title:
    #         error = 'Title is required.'
    #
    #     if error is not None:
    #         flash(error)
    #     else:
    #         db = get_db()
    #         db.execute(
    #             'INSERT INTO post (title, body, author_id)'
    #             ' VALUES (?, ?, ?)',
    #             (title, body, g.user['id'])
    #         )
    #         db.commit()
    #         return redirect(url_for('blog.index'))

    return render_template('contribute/home.html')

@bp.route('/create', methods=['GET', "POST"])
def create():
    if request.method == 'POST':
        result = request.form.to_dict(flat=True)
        capability = to_capability(result)
        talent = {}
        # print(result)
        print(capability)
        myclient = pymongo.MongoClient("mongodb://localhost:27017")
        mydb = myclient["mydatabase"]
        mycol = mydb["contribution"]
        x = mycol.insert_one(result)
    #     # body = request.form['body']
    #     post()
    return render_template('contribute/contribute.html')

def to_capability(d):
    if not d: return {}
    capability = {}
    env = []
    deploymentDetails = {}
    dataDeletionEndpointDetails = {}

    for k,v in d.items():
        if "environmentVariables_" in k:
            name = k.split("environmentVariables_")[-1]
            env.append({name : v})
        if "deploymentDetails_" in k:
            name = k.split("deploymentDetails_")[-1]
            deploymentDetails[name] = v
        if "dataDeletionEndpointDetails_" in k:
            name = k.split("dataDeletionEndpointDetails_")[-1]
            dataDeletionEndpointDetails[name] = v
        if "capability_" in k:
            name = k.split("capability_")[-1]
            capability[name] = v
    deploymentDetails["environmentVariables"] = env
    capability["deploymentDetails"] = deploymentDetails
    capability["dataDeletionEndpointDetails"] = dataDeletionEndpointDetails
    return capability