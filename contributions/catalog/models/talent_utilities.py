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

def init_talent():
    d = {
        'id': '',
        "name": '',
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

    if isinstance(d['talent_name'], str):
        talent_list.append(init_talent())
    else:
        for _ in range(len(d['talent_name'])):
            talent_list.append(init_talent())

    for i, talent in enumerate(talent_list):
        tal_id = str(uuid.uuid4())
        talent['id'] = tal_id

        for k, v in d.items():
            print(k, v)
            if "minUserPrivacyLevel" in k:
                if len(v[i]) > 0:
                    talent_list[i]["minUserPrivacyLevel"] = int(v[i])
                d[k][i] = talent_list[i]["minUserPrivacyLevel"]
            if "talent_" in k:
                name = k.split("talent_")[-1]
                # TODO this is not a very good exercise since everything is list,
                #  so the code only checks the very first items in the list assuming that
                #  the items are only single item entry.
                #  However, required capabilities should be a list so it should be handled differently,
                #  and if there is any item that is a list, that should be handled separately.
                if name in talent_list[i] and isinstance(talent_list[i][name], list) and len(v[i]) > 0:
                    if name == "requiredCapabilities":
                        for j in range(len(v)):
                            v[j] = reconstruct_required_capabilities(v[j])
                            talent_list[i][name].append(v[j])
                    else:
                        talent_list[i][name].append(v[i])
                elif name in talent_list[i] and isinstance(talent_list[i][name], list) and len(v[i]) == 0:
                    talent_list[i][name] = []
                else:
                    talent_list[i][name] = v[i]
        talent_list[i]["selfCertification"] = to_self_certification(d)
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


def to_self_certification(d):
    if not d: return {}
    res = init_self_certification()
    for k, v in d.items():
        if "selfcertificate_" in k:
            name = k.split("selfcertificate_")[-1]
            res[name] = v[0]
    return res

def reconstruct_required_capabilities(d):
    # removed \r\n
    d = json.loads(d.replace("\r\n",""))

    return d