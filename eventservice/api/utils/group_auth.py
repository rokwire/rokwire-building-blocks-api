import controllers.configs as cfg
import requests
import logging
from flask import g

logger = logging.getLogger(__name__)
ALL_GROUP_EVENTS = 'all_group-events'


def generate_groups_request():
    # Rokwire issuer token
    if g.user_token_data.get('iss') == cfg.ROKWIRE_ISSUER:
        uin = g.user_token_data.get('uiucedu_uin')
        url = "%s%s/groups" % (cfg.GROUPS_BUILDING_BLOCK_HOST + "/api/int/user/", uin)
        headers = {"Content-Type": "application/json",
                   "INTERNAL-API-KEY": cfg.INTERNAL_API_KEY}
    # Core BB Access Token, Shibboleth ID Token, etc.
    else:
        id_token = g.user_token
        url = cfg.GROUPS_BUILDING_BLOCK_HOST + "/api/user/group-memberships"
        headers = {"Content-Type": "application/json",
                   "Authorization": "Bearer " + id_token}
    return url, headers


def get_group_ids():
    group_ids = list()
    include_private_events = False
    if is_core_user_token():
        include_private_events = True
        url, headers = generate_groups_request()
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
    if is_core_user_token():
        include_private_events = True
        url, headers = generate_groups_request()
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
    if event and event.get('groupIds'):
        if len(event.get('groupIds')) != len(group_memberships):
            return False
        # check if user be the admin of all groups
        for groupId in event.get('groupIds'):
            found = False
            for group_member in group_memberships:
                if groupId == group_member.get('id') and group_member.get('role') == 'admin':
                    found = True
                    break
            if not found:
                return False
    if event and event.get('createdByGroupId'):
        found = False
        for group_member in group_memberships:
            if event.get('createdByGroupId') == group_member.get('id') and group_member.get('role') == 'admin':
                found = True
                break
        if not found:
            return False
    return True


def check_permission_access_event(event, include_private_events, group_ids):
    if include_private_events:
        # check the group id
        if event and event.get('createdByGroupId') not in group_ids:
            return False
    else:
        # check public group
        if event and event.get('isGroupPrivate') is True:
            return False
    return True


def check_all_group_event_admin():
    is_all_group_event = False
    if is_core_user_token():
        if g.user_token_data.get('permissions'):
            if g.user_token_data.get('permissions').lower().find(ALL_GROUP_EVENTS) != -1:
                is_all_group_event = True

    return is_all_group_event

def is_core_user_token():
    return 'user_token' in g and not g.user_token_data.get('anonymous') and not g.user_token_data.get('service')
