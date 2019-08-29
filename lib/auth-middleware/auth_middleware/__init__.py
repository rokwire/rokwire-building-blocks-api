import logging
import flask
import jwt
import json
import os
import requests

from flask import request, abort
from datetime import datetime
from cryptography.hazmat.primitives.asymmetric import rsa

logger = logging.getLogger(__name__)
# First cut. This is a list of secrets (eventually this can come from a database and setting it is effectively caching it)
# The zero-th element of this list is the currently active key.
# At this point we have decided that a secret is going to be a version 4 UUID.
secrets = ['2060e58d-b26d-4375-924a-05a964f9e5e8']
# The header in the request
rokwire_api_key_header = 'rokwire-api-key'
# Group names for the event and app config manager. These typically come in the is_member_of claim in the id token
rokwire_event_manager_group = 'RokwireEventManager'
rokwire_app_config_manager_group = 'RokwireAppConfigManager'

# This is the is member of claim name from the
uiucedu_is_member_of = "uiucedu_is_member_of"


def get_bearer_token(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        logger.warning("Request missing Authorization header")
        abort(401)
    ah_split = auth_header.split()
    if len(ah_split) != 2 or ah_split[0].lower() != 'bearer':
        logger.warning("invalid auth header. expecting 'bearer' and token with space between")
        abort(401)
    _id_token = ah_split[1]
    return _id_token


# Checks the id_token. This will either check the token from the UIUC Shibboleth service or a generated
# one from ROKwire for phone-based authentication.
# Use: invoke in the call. This this works, nothing happens (and processing continues) or it fails. There
# are no other options.
# This does return the id_token so that, e.g. group memberships may be checked.
def authenticate(group_name=None):

    should_use_security_token_auth = False
    app = flask.current_app
    if request.endpoint in app.view_functions:
        view_func = app.view_functions[request.endpoint]
        should_use_security_token_auth = getattr(view_func, '_use_security_token_auth', False)
    # print("should use security token auth = %s" % should_use_security_token_auth)

    auth_header = request.headers.get('Authorization')
    if not auth_header:
        logger.warning("Request missing Authorization header")
        abort(401)
    ah_split = auth_header.split()
    if len(ah_split) != 2 or ah_split[0].lower() != 'bearer':
        logger.warning("invalid auth header. expecting 'bearer' and token with space between")
        abort(401)
    _id_token = ah_split[1]
    try:
        unverified_header = jwt.get_unverified_header(_id_token)
    except jwt.exceptions.PyJWTError as jwte:
        logger.warning("jwt error on get unverified header. message = %s" % jwte)
        abort(401)
    if unverified_header.get('phone', False):
        # phone number verify
        phone_verify_secret = os.getenv('PHONE_VERIFY_SECRET')
        if not phone_verify_secret:
            logger.warning("PHONE_VERIFY_SECRET environment variable not set")
            abort(401)
        phone_verify_audience = os.getenv('PHONE_VERIFY_AUDIENCE')
        if not phone_verify_audience:
            logger.warning("PHONE_VERIFY_AUDIENCE environnment variable not set")
            abort(401)
        try:
            id_info = jwt.decode(
                _id_token,
                phone_verify_secret,
                audience=phone_verify_audience,
                verify=True
            )
        except jwt.DecodeError as de:
            logger.warning("error on id_token decode. Message = %s" % str(de))
            abort(401)
        # import pprint; pprint.pprint(id_info)
    else:
        # shibboleth
        SHIB_HOST = os.getenv('SHIBBOLETH_HOST')
        SHIB_CLIENT_ID = os.getenv('SHIBBOLETH_CLIENT_ID')
        kid = unverified_header.get('kid')
        if not kid:
            logger.warning("kid not found in unverified header")
            abort(401)
        # Comment about the next bit. The Py JWT package's support for getting the keys
        # and verifying against said key is (like the rest of it) undocumented.
        # These calls may therefore change without warning without notification in future
        # releases of that library. If this stops working, check the Py JWT libraries first.

        keyset_resp = requests.get('https://' + SHIB_HOST + '/idp/profile/oidc/keyset')
        if keyset_resp.status_code != 200:
            logger.warning("bad status getting keyset. status code = %s" % keyset_resp.status_code)
            abort(401)
        ### Next lines replace the keys for the Shib service with a locally generated set. This lets us sign id_tokens and verify them.
        # NOTE that the key file MUST only contain public keys. If there is private key information, tjhe JWT library will
        # create private keys and then explode with strange errors doing the validation. In other words, it has very poor key
        # resolution.
        file1 = open("/home/ncsa/temp/rokwire/pub_keys.jwk", "r")
        lines = file1.readlines()
        file1.close()
        my_lst_str = ''.join(map(str, lines))
        keyset = json.loads(my_lst_str)
        ### Next line is to be uncommented to re-instate using shib service keys.
        # keyset = keyset_resp.json()
        matching_jwks = [key_dict for key_dict in keyset['keys'] if key_dict['kid'] == kid]
        if len(matching_jwks) != 1:
            logger.warning("should have exactly one match for kid = %s" % kid)
            abort(401)
        jwk = matching_jwks[0]
        pub_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
        try:
            id_info = jwt.decode(_id_token, key=pub_key, audience=SHIB_CLIENT_ID, verify=True)
        except jwt.exceptions.PyJWTError as jwte:
            logger.warning("jwt error on decode. message = %s" % jwte)
            abort(401)
        if not id_info:
            logger.warning("id_info was not returned from decode")
            abort(401)
        if id_info['iss'] != 'https://' + SHIB_HOST:
            logger.warning("invalid iss of %s" % id_info['iss'])
            abort(401)
    request.user_token_data = id_info
    if (group_name != None):
        # So we are to check is a group membership is required.
        is_member_of = id_info[uiucedu_is_member_of]
        print("is_member_of" + str(is_member_of))
        if group_name not in is_member_of:
            logger.warning("user is not a member of the group " + group_name)
            abort(401)
    return id_info


# Checks that the request has the right secret for this. This call is used initially and assumes that
# the header contains the x-api-key. This (trivially) returns true of the verification worked and
# otherwise will return various other exit codes.
def verify_secret(request):
    key = request.headers.get(rokwire_api_key_header)
    if not key:
        logger.warning("Request missing the " + rokwire_api_key_header + " header")
        abort(400)  # missing header means bad request
    if (key == os.getenv('ROKWIRE_API_KEY')):
        return True
    abort(401)  # failed matching means unauthorized in this context.



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
