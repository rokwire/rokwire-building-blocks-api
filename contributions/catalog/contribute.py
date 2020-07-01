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
        # result = request.form.to_dict(flat=False)
        result = dict((key, request.form.getlist(key) if len(request.form.getlist(key)) > 1 else request.form.getlist(key)[0]) for key in request.form.keys())
        capability = to_capability(result)
        talent = to_talent(result)
        print(capability)
        print(talent)
        myclient = pymongo.MongoClient("mongodb://localhost:27017")
        mydb = myclient["mydatabase"]
        mycol = mydb["contribution"]
        x = mycol.insert_one(result)
    #     # body = request.form['body']
    #     post()
    return render_template('contribute/contribute.html')

def init_capability():
    d = {'name': '',
         'description': '',
         'apiDocUrl': '',
         'source_url': '',
         'apiBaseUrl': '',
         'version': '',
         'version_url': '',
         'healthCheckUrl': '',
         'status': '',
         'deploymentDetails': {
             'dockerImageName': '',
             'databaseDetails': '',
             'authMethod':'',
             'environmentVariables': [{"key": "","value": ""}]
         },
         'dataDeletionEndpointDetails': {
             'endpoint': '',
             'api':''
         }
         }
    return d

def to_capability(d):
    if not d: return {}
    capability_list = []

    if isinstance(d['capability_name'], str):
        capability_list.append(init_capability())
    else:
        for _ in range(len(d['capability_name'])):
            capability_list.append(init_capability())

    for i, capability in enumerate(capability_list):
        env_k, env_v = d['environmentVariables_key'], d['environmentVariables_value']
        for k,v in list(zip(env_k, env_v)):
            capability["deploymentDetails"]['environmentVariables'].append({k: v})
        for k,v in d.items():
                if "deploymentDetails_" in k:
                    name = k.split("deploymentDetails_")[-1]
                    capability_list[i]["dataDeletionEndpointDetails"][name] = v[i]
                if "dataDeletionEndpointDetails_" in k:
                    name = k.split("dataDeletionEndpointDetails_")[-1]
                    capability_list[i]["dataDeletionEndpointDetails"][name] = v[i]
                if "capability_" in k:
                    name = k.split("capability_")[-1]
                    capability[name] = v[i]
    return capability_list


def init_talent():
    d = {
    "name" : "",
    "shortDescription": "",
    "longDescription": "",
    "requiredCapabilities" :[],
    "requiredBuildingBlocks": [""],
    "minUserPrivacyLevel": 0,
    "minEndUserRoles": [""],
    "startDate": "",
    "endDate": "",
    "dataDescription": "",
    "selfCertification": {
      "dataDeletionUponRequest": "",
      "respectingUserPrivacySetting": "",
      "discloseAds": "",
      "discloseSponsors": "",
      "discloseImageRights": ""
    }
  }
    return d

def to_talent(d):
    if not d: return {}
    talent_list = []

    if isinstance(d['talent_name'], str):
        talent_list.append(init_talent())
    else:
        for _ in range(len(d['talent_name'])):
            talent_list.append(init_talent())

    for i, talent in enumerate(talent_list):
        for k,v in d.items():
                if "talent_" in k:
                    name = k.split("talent_")[-1]
                    talent[name] = v[i]
    return talent_list

def init_contribution():
    d = {
        "name": "",
        "shortDescription": "",
        "longDescription": "",
        "contributors": [],
        "capabilities" : [],
        "talents": [],
    }
    return d



def init_person():
    d = {
        "firstName": "",
        "middleName": "",
        "lastName": "",
        "email": "",
        "phone": "",
        "affiliation": {
          "name": "",
          "address": "",
          "email": "",
          "phone": ""
        }
    }
    return d


def init_organization():
    d = {
        "name": "",
        "address": "",
        "email": "",
        "phone": ""
    }
    return d