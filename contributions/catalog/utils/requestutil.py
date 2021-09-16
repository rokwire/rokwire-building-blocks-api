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

import requests
import json

from controllers.config import Config as cfg

""""
create a request header for endpoint using apikey
"""
def get_header_using_api_key():
    header = {
        'Content-Type': 'application/json',
        'rokwire-api-key': cfg.ROKWIRE_API_KEY
    }

    return header

""""
create a request header for endpoint using session
"""
def get_header_using_session(session):
    header = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + session['oauth_token']['access_token']
    }

    return header

"""
create header using auth token
"""
def get_header_using_auth_token(auth_token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + auth_token
    }

"""
request contribution list
"""
"""
request reviewer
"""
def request_contributions(headers):
    result = requests.get(cfg.CONTRIBUTION_BUILDING_BLOCK_URL, headers=headers)

    return result

""""
reuqest capability using capability id
"""
def request_capability(headers, contribution_id, cid):
    result = requests.get(cfg.CONTRIBUTION_BUILDING_BLOCK_URL +'/' + str(contribution_id) + "/capabilities/" + str(cid),
                          headers=headers)

    return result

"""
request talent using talent id
"""
def request_talent(headers, contribution_id, tid):
    result = requests.get(cfg.CONTRIBUTION_BUILDING_BLOCK_URL +'/' + str(contribution_id) + "/talents/" + str(tid),
                          headers=headers)

    return result

"""
request reviewer
"""
def request_reviewers(headers):
    result = requests.get(cfg.CONTRIBUTION_BUILDING_BLOCK_URL +'/admin/reviewers', headers=headers)

    return result

"""
request capability list
"""
def request_required_capability_list(headers):
    result = requests.get(cfg.CONTRIBUTION_BUILDING_BLOCK_URL + "/capabilities", headers=headers)

    # create the list of required capabilities
    if result.status_code == 200:
        # check if the login id is in reviewer list
        result_str = result.content.decode('utf-8').replace('\n', '')
        capability_json_list = json.loads(result_str)
        required_capability_list = []

        # create the list with only the items for required capability
        for capability_json in capability_json_list:
            contribution_id = capability_json["contributionId"]
            capability_name = capability_json["name"]
            capability_id = capability_json["id"]
            tmp_required_capability = {"contributionId": contribution_id,
                                       "capabilityName": capability_name,
                                       "capabilityId": capability_id}
            required_capability_list.append(tmp_required_capability)

    return required_capability_list