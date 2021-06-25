import controllers.configs as cfg
import requests
from flask import g

def get_group_ids():
    group_ids = list()
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
        else:
            raise Exception("failed to authorize with the groups building block %d" % req.status_code)
    return include_private_events, group_ids

def get_group_memberships():
    group_memberships = list()
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
                membership = dict()
                membership['id'] = item.get('id')
                membership['role'] = item.get('membership_status')
                group_memberships.append(membership)
        else:
            raise Exception("failed to authorize with the groups building block %d" % req.status_code)
    return include_private_events, group_memberships


# This util method checks if a user has admin permissions in a group event
def check_group_event_admin_access(event, group_memberships):
    if event and event.get('createdByGroupId'):
        found = False
        for group_member in group_memberships:
            if event.get('createdByGroupId') == group_member.get('id') and group_member.get('role') == 'admin':
                found = True
                break
        if not found:
            return False
    return True
