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

from flask import session

'''
add contributionAdmins element in the contribution json
'''


def add_contribution_admins(in_json):
    login_user = session['username']
    admin_input = in_json['contributionAdmins']

    contribution_admins = []
    # if the form input is not empty, then we want to filter out those names from there
    if admin_input:
        contribution_admins = [admin_name for admin_name in admin_input.split(',') if admin_name]

    updated_json = {"contributionAdmins": [login_user] + contribution_admins}
    in_json.update(updated_json)
    return in_json
