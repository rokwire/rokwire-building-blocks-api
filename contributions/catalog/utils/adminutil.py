#  Copyright 2020 Board of Trustees of the University of Illinois.
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

from utils import requestutil
from controllers.config import Config as cfg

"""
check if the logged in user is a superuser
"""
def check_if_superuser(login_id):
    sp_list = cfg.ADMIN_USERS.split(",")

    if login_id in sp_list:
        return True
    else:
        return False

"""
get reviewer id from given username
"""
def get_reviewer_id(headers, username):
    # check if the logged in id is in reviewers database
    # otherwise it will give 401
    reviewer_id = "None"
    result = requestutil.request_reviewers(headers)

    # if the result is not 201, it is not reviewer
    if result.status_code == 200:
        # check if the login id is in reviewer list
        result_str = result.content.decode('utf-8').replace('\n', '')
        reviewer_list = json.loads(result_str)

        # check if the user name and id
        for reviewer in reviewer_list:
            if reviewer["githubUsername"] == username:
                reviewer_id = reviewer["id"]

    return reviewer_id

"""
check if the logged in user is a reviewer
"""
def check_if_reviewer(login_id, headers):
    # check if the logged in id is in reviewers database
    # otherwise it will give 401
    result = requestutil.request_reviewers(headers)

    # if the result is not 201, it is not reviewer
    if result.status_code == 200:
        # check if the login id is in reviewer list
        result_str = result.content.decode('utf-8').replace('\n', '')
        reviewer_list = json.loads(result_str)

        # create the list with only the user name
        reviewer_name_list = []
        for reviewer in reviewer_list:
            reviewer_name_list.append(reviewer["githubUsername"])

        if login_id in reviewer_name_list:
            return True

    return False
