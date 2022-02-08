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

import json
import logging
import traceback
import requests
import datetime

from flask import (
    Blueprint, render_template, request, session, redirect, url_for
)
from requests_oauthlib import OAuth2Session
from formencode import variabledecode
from .auth import login_required
from controllers.config import Config as cfg
from utils import jsonutil
from utils import adminutil
from utils import requestutil
import models.contribution_utilities as cont_util

import os

bp = Blueprint('contribute', __name__, url_prefix=cfg.URL_PREFIX)


@bp.route('/', methods=['GET', 'POST'])
def home():
    show_sel = request.args.get('show')
    user = None
    token = None
    is_logged_in = False
    cap_json = []
    tal_json = []

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
        user = session["name"]
        token = session['oauth_token']['access_token']
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

        return render_template('contribute/home.html', git_tag=git_tag, git_sha=git_sha, cap_json=cap_json, tal_json=tal_json,
                               show_sel=show_sel, user=user)
    else:
        # query only published ones
        headers = requestutil.get_header_using_api_key()
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

        return render_template('contribute/home.html', git_tag=git_tag, git_sha=git_sha, cap_json=cap_json, tal_json=tal_json, show_sel=show_sel)

    # print("homepage.")
    # if request.method == 'POST' and request.validate_on_submit():
    #     result = request.form.to_dict(flat=False)
    # if "name" in session:
    #     return render_template('contribute/home.html', user=session["name"], token=session['oauth_token']['access_token'])
    # else:
    #     return render_template('contribute/home.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Step 1: Get the user identify for authentication.
    """
    # print("Step 1: User Authorization")
    github = OAuth2Session(cfg.GITHUB_CLIENT_ID)
    authorization_url, state = github.authorization_url(cfg.AUTHORIZATION_BASE_URL)

    # State is used to prevent CSRF.
    session['oauth_state'] = state
    return redirect(authorization_url)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('.home'))


@bp.route('/results', methods=['POST', 'GET'])
@login_required
def result():
    if request.method == 'POST':
        # result = request.form
        result = request.form.to_dict()
        query = result['search']
        search(query)
        return render_template("contribute/results.html", user=session["name"],  token=session['oauth_token']['access_token'], result=result)

@bp.route('/contributions/<contribution_id>', methods=['GET'])
def contribution_details(contribution_id):
    # check if the user is logged in
    is_logged_in = False

    try:
        # create error to see if the use is logged in or now
        # TODO this should be changed to better way
        if (session["name"] == ""):
            is_logged_in = True
        else:
            is_logged_in = True
    except:
        is_logged_in = False

    is_editor = False
    is_reviewer = False
    name = ""

    if (is_logged_in):
        # check to see if the logged in user is an editable user for creating edit button
        username = session["username"]
        name = session["name"]
        headers = requestutil.get_header_using_session(session)

        the_json_res = get_contribution(contribution_id)

        # check if the logged in user is the editor
        is_superuser = adminutil.check_if_superuser(username)
        if is_superuser:
            is_editor = True
        elif username in the_json_res["contributionAdmins"]:
            is_editor = True

        # check if the user is reviewer by requesting to endpoint
        is_reviewer = adminutil.check_if_reviewer(username, headers)
    else:
        the_json_res = get_contribution_with_api_key(contribution_id)

    return render_template("contribute/contribution_details.html", is_reviewer=is_reviewer, is_editable=is_editor,
                           post=the_json_res, user=name)

@bp.route('/contributions/<contribution_id>/edit', methods=['GET', 'POST'])
@login_required
def contribution_edit(contribution_id):
    if request.method == 'POST':
        is_put = False
        contribution_id = None
        result = request.form.to_dict(flat=False)

        # check if it is PUT
        try:
            contribution_id = result["contribution_id"][0]
            is_put = True
        except:
            s = "There is a error in edit. The method is not an edit."
            return render_template('contribute/error.html', error_msg=s)

        if is_put:
            contribution = cont_util.to_contribution(result)
            contribution = jsonutil.add_contribution_admins(contribution, is_edit=True)
            # remove id from json_data
            del contribution["id"]
            json_contribution = json.dumps(contribution, indent=4)
            response, s = put_contribution(json_contribution, contribution_id)

            if response:
                if "name" in session:
                    return render_template('contribute/submitted.html', user=session["name"],
                                           token=session['oauth_token']['access_token'])
                else:
                    return render_template('contribute/submitted.html')
            elif not response:
                if "name" in session:
                    return render_template('contribute/error.html', user=session["name"],
                                           token=session['oauth_token']['access_token'], error_msg=s)
                else:
                    return render_template('contribute/error.html', error_msg=s)
    else:
        the_json_res = get_contribution(contribution_id)
        # check if the user is editable then set the is_editable
        is_editable = False
        is_reviewer = False
        username = session["username"]
        headers = requestutil.get_header_using_session(session)

        # check if the user is in contribution's admins
        if username in the_json_res["contributionAdmins"]:
            is_editable = True

        # check if the user is a reviewer
        is_reviewer = adminutil.check_if_reviewer(username, headers)

        if is_reviewer:
            is_editable = True

        # get capability list to create required capability list
        required_capability_list = requestutil.request_required_capability_list(headers)

        if is_editable:
            return render_template('contribute/contribute.html', is_reviewer=is_reviewer, required_capabilities=required_capability_list,
                                   is_editable=is_editable, user=session["name"],
                                   token=session['oauth_token']['access_token'], post=the_json_res)
        else:
            s = "You don't have a permission to edit the contribution."
            return render_template('contribute/error.html', error_msg=s)

@bp.route('/contributions/<contribution_id>/review', methods=['GET', 'POST'])
@login_required
def contribution_review(contribution_id):
    username = session["username"]
    headers = requestutil.get_header_using_session(session)

    # check if the user is a reviewer
    is_reviewer = adminutil.check_if_reviewer(username, headers)

    if request.method == 'POST':
        is_put = False
        contribution_id = None
        result = request.form.to_dict(flat=False)

        # check if it is PUT
        try:
            contribution_status = result["contribution_status"][0]
            contribution_comment = result["contribution_reviewer_comment"][0]
            contribution_id = result["contribution_id"][0]
            is_put = True
        except:
            s = "There is a error in edit. The method is not an edit."
            return render_template('contribute/error.html', error_msg=s)

        if is_put:
            # check reviewer id from token
            reviewer_id = adminutil.get_reviewer_id(headers, username)
            if reviewer_id.lower == "none":
                s = "You don't have a permission to review the contribution."
                return render_template('contribute/error.html', error_msg=s)
            contribution_result = requestutil.request_single_contribution(headers, contribution_id)
            contribution = json.loads(contribution_result.text)

            # remove id from json_data
            del contribution["id"]

            currenttime = datetime.datetime.now()
            currenttime = currenttime.strftime("%Y/%m/%dT%H:%M:%S")

            # iterate reviews to find out the correct review location
            review_loc = 0
            if "review" in contribution.keys():
                review_list = contribution["review"]
                for idx, review_entry in enumerate(review_list):
                    if review_entry["reviewerId"] == reviewer_id:
                        review_loc = idx
                # add new elements(review_json)
                currenttime = datetime.datetime.now()
                currenttime = currenttime.strftime("%Y/%m/%dT%H:%M:%S")
                contribution["review"][review_loc]["lastUpdated"] = currenttime
                contribution["review"][review_loc]["reviewerComment"] = contribution_comment
                contribution["review"][review_loc]["reviewerId"] = reviewer_id
            else:
                # add new elements
                review_json = {'review':[{'lastUpdated': currenttime, 'reviewerComment': contribution_comment,
                                'reviewerId': reviewer_id}]}
                contribution.update(review_json)
            contribution["status"] = contribution_status
            json_contribution = json.dumps(contribution, indent=4)
            response, s = put_contribution(json_contribution, contribution_id)

            if response:
                if "name" in session:
                    return redirect(url_for('contribute.contribution_details', contribution_id=contribution_id))
                else:
                    return render_template('contribute/submitted.html')
            elif not response:
                if "name" in session:
                    return render_template('contribute/error.html', user=session["name"],
                                           token=session['oauth_token']['access_token'], error_msg=s)
                else:
                    return render_template('contribute/error.html', error_msg=s)
    else:
        the_json_res = get_contribution(contribution_id)

        # check if the user is in contribution's admins
        if username in the_json_res["contributionAdmins"]:
            is_editable = True

        # get capability list to create required capability list
        required_capability_list = requestutil.request_required_capability_list(headers)

        # if is_reviewer and is_review:
        if is_reviewer:
            # need to add review information to html so it can pre render if needed
            reviewer_id = adminutil.get_reviewer_id(headers, username)
            if "review" in the_json_res.keys():
                review_exist = False
                review_list = the_json_res["review"]
                if review_list is not None:
                    for idx, review_entry in enumerate(review_list):
                        if review_entry["reviewerId"] == reviewer_id:
                            review_loc = idx
                            review_json = {'review': review_list[review_loc]}
                            the_json_res.update(review_json)
                            break

            return render_template('contribute/contribution_details.html', is_review=True, required_capabilities=required_capability_list,
                                   user=session["name"], token=session['oauth_token']['access_token'], post=the_json_res)
        else:
            s = "You don't have a permission to review the contribution."
            return render_template('contribute/error.html', error_msg=s)

@bp.route('/contributions/<contribution_id>/capabilities/<id>', methods=['GET'])
def capability_details(contribution_id, id):
    # check if the user is logged in
    is_logged_in = False

    try:
        # create error to see if the use is logged in or now
        # TODO this should be changed to better way
        if (session["name"] == ""):
            is_logged_in = True
        else:
            is_logged_in = True
    except:
        is_logged_in = False

    is_reviewer = False
    name = ""

    if (is_logged_in):
        the_json_res = get_capability(contribution_id, id)
        is_contribution_admin = False
        username = session["username"]
        name = session["name"]
        contribution_admins = the_json_res["contributionAdmins"]
        if username in contribution_admins:
            is_contribution_admin = True
        if is_contribution_admin:
            is_reviewer = True
        else:
            # check if the user is reviewer by requesting to endpoint
            headers = requestutil.get_header_using_session(session)
            is_reviewer = adminutil.check_if_reviewer(username, headers)

        return render_template("contribute/capability_details.html", reviewer=is_reviewer, post=the_json_res, user=name)
    else:
        the_json_res = get_capability_with_api_key(contribution_id, id)
        return render_template("contribute/capability_details.html", reviewer=is_reviewer, post=the_json_res)


@bp.route('/contributions/<contribution_id>/talents/<id>', methods=['GET'])
def talent_details(contribution_id, id):
    # check if the user is logged in
    is_logged_in = False

    try:
        # create error to see if the use is logged in or now
        # TODO this should be changed to better way
        if (session["name"] == ""):
            is_logged_in = True
        else:
            is_logged_in = True
    except:
        is_logged_in = False

    is_reviewer = False
    name = ""

    if (is_logged_in):
        is_contribution_admin = False
        the_json_res = get_talent(contribution_id, id)
        username = session["username"]
        name = session["name"]
        contribution_admins = the_json_res["contributionAdmins"]
        if username in contribution_admins:
            is_contribution_admin = True

        if is_contribution_admin:
            is_reviewer = True
        else:
            # check if the user is reviewer by requesting to endpoint
            username = session["username"]
            headers = requestutil.get_header_using_session(session)
            is_reviewer = adminutil.check_if_reviewer(username, headers)

        return render_template("contribute/talent_details.html", reviewer=is_reviewer, post=the_json_res, user=name)
    else:
        the_json_res = get_talent_with_api_key(contribution_id, id)

    return render_template("contribute/talent_details.html", reviewer=is_reviewer, post=the_json_res)

# @bp.route('/edit/<contribution_id>', methods=('GET', 'POST'))
# def edit(contribution_id):
#     #todo: need to implement the edit form page
#     return render_template("contribute/contribution_details.html", contribution_json=the_json_res)

@bp.route('/contributions/create', methods=['GET', 'POST'])
@login_required
def create():
    json_contribute = None
    if request.method == 'POST':
        result = request.form.to_dict(flat=False)
        # result = dict((key, request.form.getlist(key) if len(request.form.getlist(key)) > 1 else request.form.getlist(key)[0]) for key in request.form.keys())

        contribution = cont_util.to_contribution(result)
        # add contributionAdmins to the json_contribution
        contribution = jsonutil.add_contribution_admins(contribution)
        contribution["status"] = "Submitted"
        json_contribution = json.dumps(contribution, indent=4)
        response, s, post_json = post_contribution(json_contribution)

        if response:
            return redirect(url_for('contribute.contribution_details', contribution_id=s))
        elif not response:
            logging.error(s)
            msg = "Contribution submission failed. Please try again after some time!"
            if "name" in session:
                return render_template('contribute/error.html', user=session["name"],  token=session['oauth_token']['access_token'], error_msg=msg)
            else:
                return render_template('contribute/error.html', error_msg=msg)

    # get capability list to create required capability list
    header = requestutil.get_header_using_session(session)
    required_capability_list = requestutil.request_required_capability_list(header)

    return render_template('contribute/contribute.html', required_capabilities=required_capability_list,
                           post=json_contribute, user=session["name"],  token=session['oauth_token']['access_token'])

# reviewers page
@bp.route('/contributions/reviews', methods=['GET'])
@login_required
def reviews_main():
    show_sel = request.args.get('show')
    user = None
    token = None
    is_logged_in = False
    is_editable = False
    the_res_json = None

    try:
        # create error to see if the user is logged in or now
        # TODO this should be changed to better way
        if (session["name"] == ""):
            is_logged_in = True
        else:
            is_logged_in = True
        user = session["name"]
        token = session['oauth_token']['access_token']
    except:
        is_logged_in = False

    if is_logged_in:
        # check if the user is editable then set the is_editable
        username = session["username"]
        headers = requestutil.get_header_using_session(session)
        is_editable = adminutil.check_if_reviewer(username, headers)

    if is_editable:
        result = requestutil.request_contributions(headers)
        if show_sel == None or show_sel == "all":
            # create the json for only submitted
            the_json_res = result.json()
        else:
            # create the json for keyword related
            the_json_res = jsonutil.create_status_json_from_contribution_json(result.json(), show_sel)
        return render_template('contribute/reviews.html', is_editable=is_editable, user=session["name"], token=session['oauth_token']['access_token'], post=the_json_res)
    else:
        s = "You don't have a permission to edit the contribution."
        return render_template('contribute/error.html', error_msg=s)

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

# get all contributions
def get_contributions():
    headers = requestutil.get_header_using_session(session)

    try:
        result = requests.get(cfg.CONTRIBUTION_BUILDING_BLOCK_URL, headers=headers)

        if result.status_code != 200:
            err_json = parse_response_error(result)
            logging.error("Contribution GET " + json.dumps(err_json))
            return {}

    except Exception:
        # traceback.print_exc()
        return False
    return result.json()

# post a json_data in a http request
def post_contribution(json_data):
    headers = requestutil.get_header_using_session(session)
    try:
        # Setting up post request
        result = requests.post(cfg.CONTRIBUTION_BUILDING_BLOCK_URL,
                               headers=headers,
                               data=json_data)

        if result.status_code != 200:
            err_json = parse_response_error(result)
            logging.error("Contribution POST " + json.dumps(err_json))
            err_msg = str(err_json['status']), err_json['title'], err_json['detail']
            return False, str("post method fails with error: ") + str(result.status_code) \
                   + ": " + str(err_msg)
        else:
            # parse contribution id from response
            result_str = result.content.decode("utf-8").replace("\n", "")
            contribution_id = json.loads(result_str)["id"]
            logging.info("posted ok.".format(json_data))
            return True, contribution_id, json.loads(json_data.replace("\n",""))

    except Exception:
        var = traceback.format_exc()
        return False, var, None

# PUT a json_data in a http request
def put_contribution(json_data, contribution_id):
    headers = requestutil.get_header_using_session(session)
    try:
        # set PUT url
        put_url = cfg.CONTRIBUTION_BUILDING_BLOCK_URL + "/" + contribution_id

        # Setting up post request
        result = requests.put(put_url,
                               headers=headers,
                               data=json_data)

        if result.status_code != 200:
            logging.error("PUT method failed. " + str(result.text))
            return False, str("Error Code: " + str(result.status_code) +
                              ". There was an error when editing your Contribution. Please try again later!")
        else:
            logging.info("PUT OK.".format(contribution_id))
            return True, str("Your Contribution has been successfully updated.")

    except Exception:
        traceback.print_exc()
        var = "There was an error when updating your Contribution. Please try again later!"
        return False, var

def get_contribution(contribution_id):
    headers = requestutil.get_header_using_session(session)

    try:
        if contribution_id:
            result = requests.get(cfg.CONTRIBUTION_BUILDING_BLOCK_URL + "/" + str(contribution_id),
                                  headers=headers)

        if result.status_code != 200:
            err_json = parse_response_error(result)
            logging.error("Contribution GET " + json.dumps(err_json))
            return {}
        else:
            print("GET ok.".format(contribution_id))

    except Exception:
        # traceback.print_exc()
        return False
    return result.json()

def get_contribution_with_api_key(contribution_id):
    headers = requestutil.get_header_using_api_key()

    try:
        if contribution_id:
            result = requests.get(cfg.CONTRIBUTION_BUILDING_BLOCK_URL + "/" + str(contribution_id),
                                  headers=headers)

        if result.status_code != 200:
            print("GET method fails".format(contribution_id))
            print("with error code:", result.status_code)
            return {}
        else:
            print("GET ok.".format(contribution_id))

    except Exception:
        # traceback.print_exc()
        return False
    return result.json()

def get_capability(contribution_id, cid):
    headers = requestutil.get_header_using_session(session)

    try:
        if contribution_id and cid:
            result = requestutil.request_capability(headers, contribution_id, cid)
        if result.status_code != 200:
            err_json = parse_response_error(result)
            logging.error("Capability GET " + json.dumps(err_json))
            return {}
        else:
            print("GET ok.".format(id))

    except Exception:
        # traceback.print_exc()
        return False
    return result.json()

def get_capability_with_api_key(contribution_id, cid):
    headers = requestutil.get_header_using_api_key()

    try:
        if contribution_id and cid:
            result = requestutil.request_capability(headers, contribution_id, cid)
        if result.status_code != 200:
            print("GET method fails".format(id))
            print("with error code:", result.status_code)
            return {}
        else:
            print("GET ok.".format(id))

    except Exception:
        # traceback.print_exc()
        return False
    return result.json()

def get_talent(contribution_id, tid):
    headers = requestutil.get_header_using_session(session)

    try:
        if id:
            result = requestutil.request_talent(headers, contribution_id, tid)

        if result.status_code != 200:
            err_json = parse_response_error(result)
            logging.error("Talent GET " + json.dumps(err_json))
            return {}
        else:
            print("GET ok.".format(id))

    except Exception:
        # traceback.print_exc()
        return False
    return result.json()

def get_talent_with_api_key(contribution_id, tid):
    headers = requestutil.get_header_using_api_key()

    try:
        if contribution_id and tid:
            result = requestutil.request_talent(headers, contribution_id, tid)
        if result.status_code != 200:
            print("GET method fails".format(id))
            print("with error code:", result.status_code)
            return {}
        else:
            print("GET ok.".format(id))

    except Exception:
        # traceback.print_exc()
        return False
    return result.json()

# post a json_data in a http request
def search(input_data):
    headers = requestutil.get_header_using_auth_token(cfg.AUTHENTICATION_TOKEN)

    try:
        # Setting up post request
        if not input_data or len(input_data) == 0:
            result = requests.get(cfg.CONTRIBUTION_BUILDING_BLOCK_URL + "/",
                                  headers=headers)
        else:
            result = requests.get(cfg.CONTRIBUTION_BUILDING_BLOCK_URL + "/" + str(input_data),
                                  headers=headers)

        if result.status_code != 200:
            err_json = parse_response_error(result)
            logging.error("Search " + json.dumps(err_json))
            return False
        else:
            print("posted ok.".format(input_data))
            return True

    except Exception:
        # traceback.print_exc()
        return False

"""
parse error response and convert to json object
"""
def parse_response_error(response):
    err_content = response.content.decode("utf-8").replace('\n', '')
    err_json = json.loads(err_content)

    return err_json
