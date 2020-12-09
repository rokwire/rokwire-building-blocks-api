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

import base64
import json
import logging
import os
import re

import flask
import jwt
import requests
from connexion.exceptions import OAuthProblem
from flask import request, g

logger = logging.getLogger(__name__)
# First cut. This is a list of secrets (eventually this can come from a database and setting it is effectively caching it)
# The zero-th element of this list is the currently active key.
# At this point we have decided that a secret is going to be a version 4 UUID.
# E.g. secrets = ['2060e58d-b26d-4375-924a-05a964f9e5e8']
# The header in the request
rokwire_api_key_header = 'rokwire-api-key'
# Group names for the event and app config manager. These typically come in the is_member_of claim in the id token
# rokwire_event_manager_group = 'urn:mace:' + org + \
#     ':authman:app-rokwire-service-policy-rokwire events manager'
# rokwire_events_uploader = 'urn:mace:' + org + \
#     ':authman:app-rokwire-service-policy-rokwire ems events uploader'
# rokwire_events_web_app = 'urn:mace:' + org + \
#     ':authman:app-rokwire-service-policy-rokwire events web app'
# rokwire_app_config_manager_group = 'urn:mace:' + org + \
#     ':authman:app-rokwire-service-policy-rokwire app config manager'

rokwire_event_manager_group = 'events_manager'
rokwire_events_uploader = 'events_uploader'
rokwire_events_web_app = 'events_web_app'
rokwire_app_config_manager_group = 'app_config_manager'

# This is the is member of claim name from the
is_member_of_claim = "groups"
DEBUG_ON = False


def get_bearer_token(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        logger.warning("Request missing Authorization header")
        raise OAuthProblem('Missing authorization header')
    ah_split = auth_header.split()
    if len(ah_split) != 2 or ah_split[0].lower() != 'bearer':
        logger.warning("invalid auth header. expecting 'bearer' and token with space between")
        raise OAuthProblem('Invalid request header')
    _id_token = ah_split[1]
    return _id_token


# Checks the id_token. This will either check the token from the UIUC Shibboleth service or one generated
# one from Rokwire for phone-based authentication and supporting different client applications.
# Use: invoke in the call. If this works, nothing happens (and processing continues) or it fails. There
# are no other options.
# This does return the id_token so that, e.g. group memberships may be checked.
# internal_token_only = True indicates that the incoming token is a Rokwire internal only token and it should be used
# only when the issuer is Rokwire.
# internal_token_only = False indicates that the incoming token is NOT a Rokwire internal only token and can be issued
# by any Rokwire identified issuer including itself. This is to support use cases where an action can be done by either
# a Shibboleth/phone-based user or a user using a custom client application. E.g. event creation.
def authenticate(group_name=None, internal_token_only=False):

    should_use_security_token_auth = False
    app = flask.current_app
    if request.endpoint in app.view_functions:
        view_func = app.view_functions[request.endpoint]
        should_use_security_token_auth = getattr(view_func, '_use_security_token_auth', False)
    # print("should use security token auth = %s" % should_use_security_token_auth)

    auth_header = request.headers.get('Authorization')
    if not auth_header:
        logger.warning("Request missing Authorization header")
        raise OAuthProblem('Missing authorization header')
    ah_split = auth_header.split()
    if len(ah_split) != 2 or ah_split[0].lower() != 'bearer':
        logger.warning("invalid auth header. expecting 'bearer' and token with space between")
        raise OAuthProblem('Invalid request header')
    _id_token = ah_split[1]
    id_info = verify_userauth(_id_token, group_name, internal_token_only)

    return id_info


# Checks for group membership to perform authorization
def authorize(group_name=None):

    if 'user_token_data' not in g:
        raise OAuthProblem('Token data not available for authorization. Most likely an authentication error.')
    else:
        id_info = g.user_token_data

        if group_name is not None:
            # So we are to check is a group membership is required.
            if is_member_of_claim in id_info:
                is_member_of = id_info[is_member_of_claim]
                print("groups: " + str(is_member_of))
                if group_name not in is_member_of:
                    logger.warning("user is not a member of the group " + group_name)
                    raise OAuthProblem('Invalid token')
            else:
                logger.warning(is_member_of_claim + " field is not present in the ID Token")
                raise OAuthProblem('Invalid token')


# Checks that the request has the right secret for this. This call is used initially and assumes that
# the header contains the x-api-key. This (trivially) returns true of the verification worked and
# otherwise will return various other exit codes.
def verify_secret(request):
    key = request.headers.get(rokwire_api_key_header)
    if not key:
        logger.warning("Request missing the " + rokwire_api_key_header + " header")
        raise OAuthProblem('Missing API Key')  # missing header means bad request
    # Assumption is that the key is a comma separated list of uuid's
    # This simply turns it in to a list and iterates. If the supplied key is in this list, true is returned
    # Otherwise, an error is raised.
    keys = os.getenv('ROKWIRE_API_KEY').strip().split(',')
    for test_key in keys:
        if key == test_key.strip():  # just in case there are embedded blanks
            return True
    raise OAuthProblem('Invalid API Key') # failed matching means unauthorized in this context.


def verify_apikey(key, required_scopes=None):
    if not key:
        logger.warning("API key is missing the " + rokwire_api_key_header + " header")
        raise OAuthProblem('Missing API Key')
    # Assumption is that the key is a comma separated list of uuid's
    # This simply turns it in to a list and iterates. If the supplied key is in this list, true is returned
    # Otherwise, an error is raised.
    keys = os.getenv('ROKWIRE_API_KEY').strip().split(',')
    for test_key in keys:
        if key == test_key.strip():  # just in case there are embedded blanks
            return {'token_valid': True}
    else:
        raise OAuthProblem('Invalid API Key')


def verify_userauth(id_token, group_name=None, internal_token_only=False):
    id_info = None
    if not id_token:
        logger.warning("Request missing id token")
        raise OAuthProblem('Missing id token')
    try:
        # We need to get both the header and the payload initially as unverified since we have to
        # check their issuer, key id and a few other items before we can figure out how to unpack them
        unverified_header = jwt.get_unverified_header(id_token)
        unverified_payload = jwt.decode(id_token, verify=False)
    except jwt.exceptions.PyJWTError as jwte:
        logger.warning("jwt error on get unverified header. message = %s" % jwte)
        raise OAuthProblem('Invalid token')

    issuer = unverified_payload.get('iss')
    if not issuer:
        logger.warning("Issuer not found. Aborting.")
        raise OAuthProblem('Invalid token')
    kid = unverified_header.get('kid')
    if not kid:
        logger.warning("kid not found. Aborting.")
        raise OAuthProblem('Invalid token')

    # tokenClientID = unverified_payload.get('clientID')
    # if not tokenClientID:
    #     logger.warning("clientID not found. Aborting.")
    #     raise OAuthProblem('Invalid token')
    # clientID = request.view_args.get('clientID')
    # if tokenClientID != clientID:
    #     logger.warning("clientID does not match. Aborting.")
    #     raise OAuthProblem('Invalid token to access clientID')

    valid_issuer = False
    keyset = None

    AUTH_PUBKEYS = os.getenv('AUTH_PUBKEYS', '').strip()
    AUTH_ISSUER = os.getenv('AUTH_ISSUER', '').strip()
    if issuer == AUTH_ISSUER:
        valid_issuer = True
        keyset = AUTH_PUBKEYS

    # Comment about the next bit. The Py JWT package's support for getting the keys
    # and verifying against said key is (like the rest of it) undocumented.
    # These calls may therefore change without warning without notification in future
    # releases of that library. If this stops working, check the Py JWT libraries first.
    if not valid_issuer:
        logger.warning("invalid issuer = %s" % issuer)
        raise OAuthProblem('Invalid token')

    matching_jwks = [key_dict for key_dict in keyset['keys'] if key_dict['kid'] == kid]
    if len(matching_jwks) != 1:
        logger.warning("should have exactly one match for kid = %s" % kid)
        raise OAuthProblem('Invalid token')
    jwk = matching_jwks[0]
    pub_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
    try:
        id_info = jwt.decode(id_token, key=pub_key, verify=True)
    except jwt.exceptions.PyJWTError as jwte:
        logger.warning("jwt error on decode. message = %s" % jwte)
        raise OAuthProblem('Invalid token')
    if not id_info:
        logger.warning("id_info was not returned from decode")
        raise OAuthProblem('Invalid token')
    # Store ID info for future references in the current request context.
    g.user_token_data = id_info

    return id_info


def use_security_token_auth(func):
    func._use_security_token_auth = True
    return func


# def authenticate_google():
#     from google.oauth2 import id_token
#     from google.auth.transport import requests as google_auth_requests

#     _id_token = request.headers.get('Id-Token')
#     if not _id_token:
#         logger.warning("Request missing Id-Token header")
#         abort(401)
#     client_platform = request.headers.get('Client-Platform')
#     if not client_platform:
#         logger.warning("Request missing Client-Platform header")
#         abort(401)
#     if client_platform == 'android':
#         client_id = '995345377706-jo1h6i34bm6k2gce2018an17iohe2ouf.apps.googleusercontent.com'
#     elif client_platform == 'ios':
#         client_id = '995345377706-8rti0kckia00gnv0kn56btrcbgour92a.apps.googleusercontent.com'
#     else:
#         logger.warning("unrecognized client platform of %s" % client_platform)
#         abort(401)
#     try:
#         id_info = id_token.verify_oauth2_token(
#             _id_token,
#             google_auth_requests.Request(),
#             client_id,
#         )
#     except ValueError as ve:
#         logger.warning("ValueError on token verify. Message = %s" % ve)
#         abort(401)
#     if not id_info:
#         logger.warning("token not verified")
#         abort(401)
#     if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
#         logger.warning("invalid iss of %s" % id_info['iss'])
#         abort(401)
#     if id_info['hd'] != 'illinois.edu':
#         logger.warning("unrecognized host domain of %s" % id_info['hd'])
#         abort(401)
#     request.user_token_data = id_info
#     return
