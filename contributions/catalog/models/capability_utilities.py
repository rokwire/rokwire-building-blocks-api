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
    # this should be checked keys that is as suffix of _number
    num_cap = 0
    # if there is capability_name_{num}, it means that there is capability
    capability_pattern = re.compile('capability_name_[0-9]')
    keys = list(d.keys())
    if any(capability_pattern.match(key) for key in keys):
        cap_indexes = []
        # iterate to count the number of capabilities
        for key in keys:
            key_splitted = key.split("capability_name_")
            if len(key_splitted) > 1:
                cap_indexes.append(int(key_splitted[1]))
        num_cap = len(cap_indexes)

        # init capability
        for _ in range(num_cap):
            capability_list.append(init_capability())
    for ind, capability in enumerate(capability_list):
        cap_id = str(uuid.uuid4())
        capability['id'] = cap_id
        i = cap_indexes[ind]
        # get environment key value pairs by pattern matching.
        # filter by matching with pattern environmentVariables_key_{{env_num}}_{{cap_num}}
        key_pattern = re.compile('environmentVariables_key_[0-99]+' + '_' + str(i))
        val_pattern = re.compile('environmentVariables_value_[0-99]+' + '_' + str(i))
        d_keys = list(filter(key_pattern.match, d))  # filter keys matching pattern
        d_vals = list(filter(val_pattern.match, d))  # filter keys matching pattern
        # iterate to get key and value pairs if exist
        if d_keys and d_vals:
            for k, v in zip(d_keys, d_vals):
                # get and append the values if they are not empty
                if d[k][0]:
                    capability["deploymentDetails"]['environmentVariables'].append({'key': d[k][0], 'value': d[v][0]})

        for k, v in d.items():
            if "isOpenSource_" + str(i) in k:
                if v[0] == 'y':
                    capability_list[ind]["isOpenSource"] = True
                else:
                    capability_list[ind]["isOpenSource"] = False
                d[k][0] = capability_list[ind]["isOpenSource"]
            elif "sourceRepoUrl_" + str(i) in k:
                if capability_list[ind]["isOpenSource"]:
                    capability_list[ind]["sourceRepoUrl"] = v[0]
            elif "deploymentDetails_" in k:
                if ("_" + str(i)) in k:
                    name = (k.split("deploymentDetails_")[-1]).split('_' + str(i))[0]
                    capability_list[ind]["deploymentDetails"][name] = v[0]
            elif "dataDeletionEndpointDetails_" in k:
                if ("_" + str(i)) in k:
                    name = (k.split("dataDeletionEndpointDetails_")[-1]).split('_' + str(i))[0]
                    capability_list[ind]["dataDeletionEndpointDetails"][name] = v[0]
            elif "capability_" in k:
                if ("_" + str(i)) in k:
                    name = (k.split("capability_")[-1]).split('_' + str(i))[0]
                    if name in capability_list[ind] and isinstance(capability_list[ind][name], list) and len(v[0]) > 0:
                        capability_list[ind][name].append(v[0])
                    elif name in capability_list[ind] and isinstance(capability_list[ind][name], list) and len(v[0]) == 0:
                        capability_list[ind][name] = []
                    else:
                        capability_list[ind][name] = v[0]

    return capability_list
