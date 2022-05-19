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

from .capability_utilities import to_capability
from .talent_utilities import to_talent


def init_contribution():
    d = {
        "name": '',
        "shortDescription": '',
        "longDescription": '',
        'contributionAdmins': [],
        "contributors": [],
        "contacts": '',
        "capabilities": [],
        "talents": []
    }
    return d


def init_person():
    return {
        "contributorType": "",
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


def init_organization():
    return {
        "contributorType": "",
        "name": "",
        "address": "",
        "email": "",
        "phone": ""
    }


def to_contributor(d):
    if not d: return {}
    # person_list = []
    # org_list = []
    contributor_list = []
    # num_contributor = 0

    # if there is contributor_type_0, it means that there is capability
    if 'contributor_type_0' in d.keys():
        # keys = list(d.keys())
        contributor_len = []

        # iterate to count the number of contributors
        for key, value in d.items():
            key_splitted = key.split("contributor_type_")
            if len(key_splitted) > 1:
                contributor_len.append(int(key_splitted[1]))
                if value[0] == "person":
                    contributor_list.append(init_person())
                elif value[0] == "organization":
                    contributor_list.append(init_organization())
        # num_contributor = max(contributor_len) + 1

    # init contributor
    # for i in range(num_contributor):
    #     # todo separate person and organization
    #     # if d[i]["contributor_type"]:
    #     #     contributor_list.append(init_organization())
    for k, v in d.items():
        if "person_" in k.lower():
            name = k.split("person_")[-1]
            splitted_key = name.split("_")
            if len(splitted_key) > 1:    # means there is some number tag after '_'
                index = int(splitted_key[-1])
                name = splitted_key[0]
                contributor_list[index][name] = v[0]
        if "affiliation_" in k.lower():
            name = k.split("affiliation_")[-1]
            splitted_key = name.split("_")
            if len(splitted_key) > 1:    # means there is some number tag after '_'
                index = int(splitted_key[-1])
                name = splitted_key[0]
                contributor_list[index]["affiliation"][name] = v[0]
        if "org_" in k.lower():
            name = k.split("org_")[-1]
            splitted_key = name.split("_")
            if len(splitted_key) > 1:    # means there is some number tag after '_'
                index = int(splitted_key[-1])
                name = splitted_key[0]
                contributor_list[index][name] = v[0]
        if "contributor_type_" in k.lower():
            splitted_key = k.split("contributor_type_")
            if len(splitted_key) > 1:    # means there is some number tag after '_'
                index = int(splitted_key[-1])
                contributor_list[index]["contributorType"] = v[0]

    return contributor_list


def init_contact():
    d = {"name": "",
         "email": "",
         "phone": "",
         "organization": "",
         "officialAddress": ""
         }
    return d


def to_contact(d):
    if not d: return {}
    res = [init_contact()]
    for cont in res:
        for k, v in d.items():
            if "contact_" in k:
                name = k.split("contact_")[-1]
                # print(name, v)
                cont[name] = v[0]
    return res


def to_contribution(d):
    if not d: return {}
    res = init_contribution()
    capability = to_capability(d)
    if len(capability) >= 1 and capability[0]["name"]:
        res["capabilities"] = capability
    # print(res["capabilities"])
    talent = to_talent(d)
    if len(talent) >= 1 and talent[0]["name"]:
        res["talents"] = talent
    contributor = to_contributor(d)
    res["contributors"] = contributor
    contact = to_contact(d)
    res["contacts"] = contact

    for k, v in d.items():
        if "contribution_" in k:
            name = k.split("contribution_")[-1]
            res[name] = v[0]

    return res
