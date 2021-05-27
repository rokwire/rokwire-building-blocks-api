import controllers.configs as cfg
import requests
from flask import g

def get_group_ids(group_ids):
    include_private_events = False
    # user UserAuth request
    if 'user_token_data' in g:
        include_private_events = True
        auth_resp = g.user_token_data
        uin = auth_resp.get('uiucedu_uin')
        url = "%s%s/groups" % (cfg.GROUPS_BUILDING_BLOCK_ENDPOINT, uin)
        headers = {"Content-Type": "application/json",
                  "ROKWIRE_GS_API_KEY": cfg.ROKWIRE_GROUPS_API_KEY}

        req = requests.get(url, headers=headers)
        if req.status_code == 200:
            req_data = req.json()
            for item in req_data:
                group_ids.append(item.get('id'))
    return include_private_events