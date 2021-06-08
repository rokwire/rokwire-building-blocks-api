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
import logging

from flask import request

import contributions.api.utils.jsonutils as jsonutils
import contributions.api.utils.datasetutils as datasetutils

from contributions.api.models.person import Person
from contributions.api.models.organization import Organization
from contributions.api.models.capabilities.capability import Capability
from contributions.api.models.talents.talent import Talent


def construct_capability(in_json):
    # new installation of the app
    capability_dataset = Capability('')
    capability_dataset, restjson = datasetutils.update_capability_dataset_from_json(capability_dataset, in_json)

    return capability_dataset, restjson, None

def construct_talent(in_json):
    is_required_field = True
    error_required = ""
    try:
        error_required = "name"
        name = in_json["name"]
        error_required = "shortDescription"
        description = in_json["shortDescription"]
    except:
        msg = {
            "reason": "Some of the required field in talent is not provided: " + str(error_required),
            "error": "Bad Request: " + request.url,
        }
        msg_json = jsonutils.create_log_json("Contribution", "POST", msg)
        logging.error("Contribution POST " + json.dumps(msg_json))
        return None, None, msg_json

    # new installation of the app
    talent_dataset = Talent('')
    talent_dataset, restjson = datasetutils.update_talent_dataset_from_json(talent_dataset, in_json)

    return talent_dataset, restjson, None

def construct_contributors(in_json):
    # need to know if it is person or organization
    # TODO make better algorithm for this, but for now use if there is firstname or lastname it is a Person, otherwise, organization

    is_person = False
    try:
        firstname = in_json["firstName"]
        is_person = True
    except:
        pass
    try:
        lastname = in_json["lastName"]
        is_person = True
    except:
        pass

    contributor_dataset = None
    if is_person:
        contributor_dataset = Person('')
        contributor_dataset, restjson = datasetutils.update_person_dataset_from_json(contributor_dataset, in_json)
        # set affiliation
        try:
            affilication_json = in_json['affiliation']
            affilication_dataset = Organization('')
            affilication_dataset, restjson = datasetutils.update_organization_dataset_from_json(affilication_dataset, affilication_json)
            contributor_dataset.set_affilication(affilication_dataset)
            del restjson['affiliation']
        except:
            pass
    else: # organization
        contributor_dataset = Organization('')
        contributor_dataset, restjson = datasetutils.update_organization_dataset_from_json(contributor_dataset, in_json)

    return contributor_dataset, restjson, None