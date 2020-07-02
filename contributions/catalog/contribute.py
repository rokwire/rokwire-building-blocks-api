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
        result = request.form.to_dict(flat=False)
        # result = dict((key, request.form.getlist(key) if len(request.form.getlist(key)) > 1 else request.form.getlist(key)[0]) for key in request.form.keys())
        contribution = to_contribution(result)
        print(contribution)
        myclient = pymongo.MongoClient("mongodb://localhost:27017")
        mydb = myclient["mydatabase"]
        mycol = mydb["contribution"]
        x = mycol.insert_one(contribution)
    #     # body = request.form['body']
    #     post()
    return render_template('contribute/contribute.html')

def init_capability():
    d = {'name': '',
         'description': '',
         'apiDocUrl': '',
         'isOpenSource': '',
         'apiBaseUrl': '',
         'version': '',
         'healthCheckUrl': '',
         'status': '',
         'deploymentDetails': {
             'dockerImageName': '',
             'databaseDetails': '',
             'authMethod':'',
             'environmentVariables': []
         },
         'dataDeletionEndpointDetails': {
             'endpoint': '',
             'api':''
         },
         "contacts" : [],
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
            capability["deploymentDetails"]['environmentVariables'].append({'key': k, 'value': v})
        for k,v in d.items():
                if "deploymentDetails_" in k:
                    name = k.split("deploymentDetails_")[-1]
                    capability_list[i]["dataDeletionEndpointDetails"][name] = v[i]
                if "dataDeletionEndpointDetails_" in k:
                    name = k.split("dataDeletionEndpointDetails_")[-1]
                    capability_list[i]["dataDeletionEndpointDetails"][name] = v[i]
                if "capability_" in k:
                    name = k.split("capability_")[-1]
                    capability_list[i][name] = v[i]
    return capability_list


def init_talent():
    d = {
    "name" : "",
    "shortDescription": "",
    "longDescription": "",
    "requiredCapabilities" :[],
    "requiredBuildingBlocks": [],
    "minUserPrivacyLevel": 0,
    "minEndUserRoles": [],
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
                    talent_list[i][name] = v[i]
    return talent_list

def init_contribution():
    d = {
        "name": "",
        "shortDescription": "",
        "longDescription": "",
        "contributors": [],
        "capabilities" : [],
        "talents": []
    }
    return d

def to_contribution(d):
    if not d: return {}
    res = init_contribution()
    capability = to_capability(d)
    res["capabilities"] = capability
    talent = to_talent(d)
    res["talents"] = talent
    contributor = to_contributor(d)
    res["contributors"] = contributor

    for k, v in d.items():
        if "contribution_" in k:
            name = k.split("contribution_")[-1]
            res[name] = v[0]
    return res

def to_contributor(d):
    def init_person():
        return {
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
    def init_organization(): return {
            "name": "",
            "address": "",
            "email": "",
            "phone": ""
        }

    if not d: return {}
    person_list = []
    org_list = []

    if 'org_name' in d:
        if isinstance(d['org_name'], str):
            org_list.append(init_organization())
        else:
            for _ in range(len(d['org_name'])):
                org_list.append(init_organization())

    if 'person_firstName' in d:
        if isinstance(d['person_firstName'], str):
            person_list.append(init_person())
        else:
            for _ in range(len(d['person_firstName'])):
                person_list.append(init_person())

    for i, e in enumerate(person_list):
        for k,v in d.items():
                if "affiliation_" in k.lower():
                    # print(k,v)
                    name = k.split("affiliation_")[-1]
                    person_list[i]["affiliation"][name] = v[i]
                if "person_" in k.lower():
                    name = k.split("person_")[-1]
                    person_list[i][name] = v[i]
    # print(person_list)

    for i, e in enumerate(org_list):
        for k,v in d.items():
                if "org_" in k:
                    name = k.split("org_")[-1]
                    org_list[i][name] = v[i]

    if not person_list or len(person_list) == 0: return org_list
    if not org_list or len(person_list) == 0: return person_list
    return person_list + org_list

def init_contact():
    d = {
            "name": "",
            "email": "",
            "phone": "",
            "organization": "",
            "officialAddress": ""
        }
