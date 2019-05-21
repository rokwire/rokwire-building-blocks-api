import logging

from flask import request, abort
from google.oauth2 import id_token
from google.auth.transport import requests as google_auth_requests

logger = logging.getLogger(__name__)

def authenticate():
    _id_token = request.headers.get('Id-Token')
    if not _id_token:
        logger.warn("Request missing Id-Token header")
        abort(401)
    client_platform = request.headers.get('Client-Platform')
    if not client_platform:
        logger.warn("Request missing Client-Platform header")
        abort(401)
    if client_platform == 'android':
        client_id = '995345377706-jo1h6i34bm6k2gce2018an17iohe2ouf.apps.googleusercontent.com'
    elif client_platform == 'ios':
        client_id = '995345377706-8rti0kckia00gnv0kn56btrcbgour92a.apps.googleusercontent.com'
    else:
        logger.warn("unrecognized client platform of %s" % client_platform)
        abort(401)
    try:
        id_info = id_token.verify_oauth2_token(
            _id_token,
            google_auth_requests.Request(),
            client_id,
        )
    except ValueError as ve:
        logger.warn("ValueError on token verify. Message = %s" % ve)
        abort(401)
    if not id_info:
        logger.warn("token not verified")
        abort(401)
    if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        logger.warn("invalid iss of %s" % id_info['iss'])
        abort(401)
    if id_info['hd'] != 'illinois.edu':
        logger.warn("unrecognized host domain of %s" % id_info['hd'])
        abort(401)
    request.user_token_data = id_info
