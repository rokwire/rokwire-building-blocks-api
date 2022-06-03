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

import uuid
import re

def init_capability():
    d = {'id': '',
         'name': '',
         'description': '',
         'icon': None,
         'apiDocUrl': None,
         'isOpenSource': None,
         'sourceRepoUrl': '',
         'apiBaseUrl': None,
         'version': '',
         'healthCheckUrl': None,
         'status': None,
         'deploymentDetails': {
             'location': '',
             'dockerImageName': None,
             'databaseDetails': None,
             'authMethod': None,
             'environmentVariables': []
         },
         'dataDeletionEndpointDetails': {
             'deletionEndpoint': '',
             'apiKey': '',
             'description': ''
         },
         }
    return d


def to_capability(d):
    if not d: return {}
    capability_list = []

    # check how many capabilities are in the given json
    # this should be checked keys that is as surfix of _number
    num_cap = 0
    # if there is capability_name_0, it means that there is capability
    if "capability_name_0" in d:
        keys = list(d.keys())
        cap_len = []
        # iterate to count the number of capabilities
        for key in keys:
            key_splitted = key.split("capability_name_")
            if len(key_splitted) > 1:
                cap_len.append(int(key_splitted[1]))
        num_cap = max(cap_len) + 1

        # init capability
        for _ in range(num_cap):
            capability_list.append(init_capability())
    for i, capability in enumerate(capability_list):
        cap_id = str(uuid.uuid4())
        capability['id'] = cap_id
        key_pattern = re.compile('environmentVariables_key_[0-9]+' + '_' + str(i))
        val_pattern = re.compile('environmentVariables_value_[0-9]+' + '_' + str(i))
        d_keys = list(filter(key_pattern.match, d))  # filter keys matching pattern
        d_vals = list(filter(val_pattern.match, d))  # filter keys matching pattern
        for k, v in zip(d_keys, d_vals):
                capability["deploymentDetails"]['environmentVariables'].append({'key': d[k][0], 'value': d[v][0]})

        for k, v in d.items():
            if "isOpenSource_" + str(i) in k:
                if v[0] == 'y':
                    capability_list[i]["isOpenSource"] = True
                else:
                    capability_list[i]["isOpenSource"] = False
                d[k][0] = capability_list[i]["isOpenSource"]
            elif "sourceRepoUrl_" + str(i) in k:
                if capability_list[i]["isOpenSource"]:
                    capability_list[i]["sourceRepoUrl"] = v[0]
            elif "deploymentDetails_" in k:
                if ("_" + str(i)) in k:
                    name = (k.split("deploymentDetails_")[-1]).split('_' + str(i))[0]
                    capability_list[i]["deploymentDetails"][name] = v[0]
            elif "dataDeletionEndpointDetails_" in k:
                if ("_" + str(i)) in k:
                    name = (k.split("dataDeletionEndpointDetails_")[-1]).split('_' + str(i))[0]
                    capability_list[i]["dataDeletionEndpointDetails"][name] = v[0]
            elif "capability_" in k:
                if ("_" + str(i)) in k:
                    name = (k.split("capability_")[-1]).split('_' + str(i))[0]
                    if name in capability_list[i] and isinstance(capability_list[i][name], list) and len(v[0]) > 0:
                        capability_list[i][name].append(v[0])
                    elif name in capability_list[i] and isinstance(capability_list[i][name], list) and len(v[0]) == 0:
                        capability_list[i][name] = []
                    else:
                        capability_list[i][name] = v[0]

    return capability_list
