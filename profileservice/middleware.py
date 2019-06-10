import logging

from flask import request, abort

logger = logging.getLogger(__name__)


def authenticate_shibboleth():
    import jwt
    import json
    import requests

    SHIB_HOST = 'shibboleth-test.techservices.illinois.edu'

    _id_token = request.headers.get('Id-Token')
    if not _id_token:
        logger.warning("Request missing Id-Token header")
        abort(401)
    kid = jwt.get_unverified_header(_id_token)['kid']
    keyset_resp = requests.get('https://' + SHIB_HOST + '/idp/profile/oidc/keyset')
    if keyset_resp.status_code != 200:
        logger.warning("bad status getting keyset. status code = %s" % keyset_resp.status_code)
        abort(401)
    keyset = keyset_resp.json()
    matching_jwks = [key_dict for key_dict in keyset['keys'] if key_dict['kid'] == kid]
    if len(matching_jwks) != 1:
        logger.warning("should have exactly one match for kid = %s" % kid)
        abort(401)
    jwk = matching_jwks[0]
    pub_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
    try:
        id_info = jwt.decode(_id_token, key=pub_key, audience="rokwire-auth-poc")
    except jwt.exceptions.DecodeError as de:
        logger.warning("decode error. message = %s" % de)
        abort(401)
    if not id_info:
        logger.warning("id_info was not returned from decode")
        abort(401)
    if id_info['iss'] not in [SHIB_HOST, 'https://' + SHIB_HOST,]:
        logger.warning("invalid iss of %s" % id_info['iss'])
        abort(401)
    request.user_token_data = id_info
    return


def authenticate_google():
    from google.oauth2 import id_token
    from google.auth.transport import requests as google_auth_requests

    _id_token = request.headers.get('Id-Token')
    if not _id_token:
        logger.warning("Request missing Id-Token header")
        abort(401)
    client_platform = request.headers.get('Client-Platform')
    if not client_platform:
        logger.warning("Request missing Client-Platform header")
        abort(401)
    if client_platform == 'android':
        client_id = '995345377706-jo1h6i34bm6k2gce2018an17iohe2ouf.apps.googleusercontent.com'
    elif client_platform == 'ios':
        client_id = '995345377706-8rti0kckia00gnv0kn56btrcbgour92a.apps.googleusercontent.com'
    else:
        logger.warning("unrecognized client platform of %s" % client_platform)
        abort(401)
    try:
        id_info = id_token.verify_oauth2_token(
            _id_token,
            google_auth_requests.Request(),
            client_id,
        )
    except ValueError as ve:
        logger.warning("ValueError on token verify. Message = %s" % ve)
        abort(401)
    if not id_info:
        logger.warning("token not verified")
        abort(401)
    if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        logger.warning("invalid iss of %s" % id_info['iss'])
        abort(401)
    if id_info['hd'] != 'illinois.edu':
        logger.warning("unrecognized host domain of %s" % id_info['hd'])
        abort(401)
    request.user_token_data = id_info
    return
