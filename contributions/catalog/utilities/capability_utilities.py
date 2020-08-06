def init_capability():
    d = {'name': '',
         'description': '',
         'icon': None,
         'apiDocUrl': None,
         'isOpenSource': False,
         'sourceUrl': '',
         'apiBaseUrl': None,
         'version': None,
         'healthCheckUrl': None,
         'status': None,
         'deploymentDetails': {
             'location': '',
             'dockerImageName': '',
             'databaseDetails': '',
             'authMethod': '',
             'environmentVariables': []
         },
         'dataDeletionEndpointDetails': {
             'endpoint': '',
             'api': ''
         },
         }
    return d


def to_capability(d):
    if not d: return {}
    capability_list = []

#init capability
    if isinstance(d['capability_name'], str):
        capability_list.append(init_capability())
    else:
        for _ in range(len(d['capability_name'])):
            capability_list.append(init_capability())

    for i, capability in enumerate(capability_list):
        env_k, env_v = d['environmentVariables_key'], d['environmentVariables_value']
        for k, v in list(zip(env_k, env_v)):
            capability["deploymentDetails"]['environmentVariables'].append({'key': k, 'value': v})

        for k, v in d.items():
            if "isOpenSource" in k:
                if v[i] == 'on':
                    capability_list[i]["isOpenSource"] = True
                else:
                    capability_list[i]["isOpenSource"] = False
                d[k][i] = capability_list[i]["isOpenSource"]
            elif "deploymentDetails_" in k:
                name = k.split("deploymentDetails_")[-1]
                capability_list[i]["deploymentDetails"][name] = v[i]
            elif "dataDeletionEndpointDetails_" in k:
                name = k.split("dataDeletionEndpointDetails_")[-1]
                capability_list[i]["dataDeletionEndpointDetails"][name] = v[i]
            elif "capability_" in k:
                name = k.split("capability_")[-1]
                if name in capability_list[i] and isinstance(capability_list[i][name], list) and len(v[i]) > 0:
                    capability_list[i][name].append(v[i])
                elif name in capability_list[i] and isinstance(capability_list[i][name], list) and len(v[i])==0:
                    capability_list[i][name] = []
                else:
                    capability_list[i][name] = v[i]
        capability_list[i]["contacts"] = to_contact(d)

    return capability_list


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
                print(name, v)
                cont[name] = v[0]
    return res
