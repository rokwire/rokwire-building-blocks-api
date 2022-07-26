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

from datetime import date
import uuid
import json
import re

def init_talent():
    d = {
        'id': '',
        "name": '',
        "icon": None,
        "shortDescription": '',
        "longDescription": '',
        "requiredCapabilities": [],
        "requiredBuildingBlocks": [],
        "minUserPrivacyLevel": 1,
        "minEndUserRoles": [],
        "startDate": date.today().strftime("%d/%m/%Y"),
        "endDate": date.today().strftime("%d/%m/%Y"),
        "dataDescription": ''
    }
    return d


def to_talent(d):
    if not d: return {}
    talent_list = []

    # check how many capabilities are in the given json
    # this should be checked keys that is as suffix of _number
    num_tal = 0
    # if there is capability_name_{num}, it means that there is capability
    talent_pattern = re.compile('talent_name_[0-9]')
    keys = list(d.keys())
    if any(talent_pattern.match(key) for key in keys):
        tal_indexes = []
        # iterate to count the number of capabilities
        for key in keys:
            key_splitted = key.split("talent_name_")
            if len(key_splitted) > 1:
                tal_indexes.append(int(key_splitted[1]))
        num_tal = len(tal_indexes)

        # init capability
        for _ in range(num_tal):
            talent_list.append(init_talent())

    for ind, talent in enumerate(talent_list):
        tal_id = str(uuid.uuid4())
        talent['id'] = tal_id
        i = tal_indexes[ind]
        for k, v in d.items():
            if "minUserPrivacyLevel_" in k:
                if len(str(v[0])) > 0:
                    talent_list[i]["minUserPrivacyLevel"] = int(v[0])
                d[k][0] = talent_list[i]["minUserPrivacyLevel"]
            if "talent_" in k:
                if ("_" + str(i)) in k:
                    name = (k.split("talent_")[-1]).split('_' + str(i))[0]
                    # TODO this is not a very good exercise since everything is list,
                    #  so the code only checks the very first items in the list assuming that
                    #  the items are only single item entry.
                    #  However, required capabilities should be a list so it should be handled differently,
                    #  and if there is any item that is a list, that should be handled separately.
                    if name in talent_list[ind] and isinstance(talent_list[ind][name], list) and len(v[0]) > 0:
                        if name == "requiredCapabilities":
                            for j in range(len(v)):
                                v[j] = reconstruct_required_capabilities(v[j])
                                talent_list[ind][name].append(v[j])
                        elif name == "requiredBuildingBlocks":
                            for j in range(len(v)):
                                talent_list[ind][name].append(v[j])
                        elif name == "minEndUserRoles":
                            for j in range(len(v)):
                                talent_list[ind][name].append(v[j])
                        else:
                            talent_list[ind][name].append(v[i])
                    elif name in talent_list[ind] and isinstance(talent_list[ind][name], list) and len(v[0]) == 0:
                        talent_list[ind][name] = []
                    else:
                        talent_list[ind][name] = v[0]

        talent_list[ind]["selfCertification"] = to_self_certification(d, i)

    return talent_list

def init_self_certification():
    d = {
        "dataDeletionUponRequest": '',
        "respectingUserPrivacySetting": '',
        "discloseAds": '',
        "discloseSponsors": '',
        "discloseImageRights": ''
        }

    return d


def to_self_certification(d, i):
    if not d: return {}
    res = init_self_certification()
    for k, v in d.items():
        if "selfcertificate_" in k:
            if ("_" + str(i)) in k:
                name = (k.split("selfcertificate_")[-1]).split('_' + str(i))[0]
                res[name] = v[0]
    return res

def reconstruct_required_capabilities(d):
    # removed \r\n
    d = json.loads(d.replace("\r\n",""))

    return d
