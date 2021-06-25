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

import controllers.configs as cfg
# import contributions.api.utils.mongoutils as mongoutils

def check_if_superuser(login_id):
    return "test"

def check_if_reviewer(login_id):
    is_reviewer = False

    # TODO if you want to allow the reviewers to do the reviewer admin,
    #  activate following code block
    # check if the logged in id is in reviewers database
    # list_reviewers = mongoutils.list_reviewers()
    #
    # if list_reviewers is not None:
    #     is_reviewer = True
    #
    #     return is_reviewer

    # check if the logged in id is admin user
    is_superuser = check_if_superuser(login_id)
    sp_list = cfg.ADMIN_USERS.split(",")

    if login_id in sp_list:
        return True
    else:
        return False

    return False