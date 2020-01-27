import re
import flask
from bson import ObjectId
from flask import request, make_response

from . import dbutils

app = flask.Flask(__name__)


# SUCCESS REQUEST HANDLER
def success_response(status_code, msg, app_config_id):
    message = {
        'status': status_code,
        'id': app_config_id,
        'message': msg
    }
    resp = flask.jsonify(message)
    resp.status_code = status_code
    return make_response(resp)


# @bp.errorhandler(400)
# BAD REQUEST ERROR HANDLER
@app.errorhandler(400)
def server_400_error(error=None):
    if error is None:
        error = {
            'error': 'Bad Request: ' + request.url,
        }
    resp = flask.jsonify(error)
    resp.status_code = 400
    return resp


# @bp.errorhandler(401)
# UNAUTHORIZED ERROR HANDLER
@app.errorhandler(400)
def server_401_error(error=None):
    if error is None:
        error = {
            'message': 'Unauthorized : ' + request.url,
        }
    resp = flask.jsonify(error)
    resp.status_code = 401
    return resp


# @bp.errorhandler(404)
# NOT FOUND ERROR HANDLER
@app.errorhandler(404)
def server_404_error(error=None):
    if error is None:
        error = {
            'message': 'App config not found : ' + request.url + '. If search by mobile api version, please check the given version conforms major.minor.patch format, for example, 1.2.0',
        }
    resp = flask.jsonify(error)
    resp.status_code = 404
    return resp


# @bp.errorhandler(405)
@app.errorhandler(405)
# INVALID INPUT ERROR HANDLER
def server_405_error(error=None):
    if error is None:
        error = {
            'message': 'Invalid input : ' + request.url,
        }
    resp = flask.jsonify(error)
    resp.status_code = 405
    return resp


# @bp.errorhandler(500)
# INTERNAL ERROR HANDLER
@app.errorhandler(500)
def server_500_error(error=None):
    if error is None:
        message = {
            'message': 'Internal error : ' + request.url,
        }
    resp = flask.jsonify(message)
    resp.status_code = 500
    return resp


def format_query(args, query):
    """
    If mobileAppVersion parameter is given, we order by version numbers since natural order of mobileAppVersion string does not work.
    For example 10.0.1 and 5.9.80, natural order, query = {'mobileAppVersion': {'$lte': version}}, will place 5.9.80 first.
    In reality, we are looking for 10.0.1 being the first

    :param args: for getting mobile version
    :param query: input query
    :return: a formatted query
    """
    version = args.get('mobileAppVersion')
    if version is not None and dbutils.check_appversion_format(version):
        m = re.match(dbutils.VERSION_NUMBER_REGX, version)
        query = {'$or': [
            {'version_numbers.major': {'$lt': int(m.group(1))}},
            {'$and': [{'version_numbers.major': {'$eq': int(m.group(1))}},
                      {'version_numbers.minor': {'$lt': int(m.group(2))}}]},
            {'$and': [{'version_numbers.major': {'$eq': int(m.group(1))}},
                      {'version_numbers.minor': {'$eq': int(m.group(2))}},
                      {'version_numbers.patch': {'$lte': int(m.group(3))}}]}
        ]}
    return query


# to add a new mobile version in db
def add_version_numbers(req_data):
    version = req_data['mobileAppVersion']
    version_numbers = dbutils.create_version_numbers(version)
    req_data['version_numbers'] = version_numbers


def check_format(req_data):
    """
    Check if any one of them is invalid:
        - mobile version & format in the db
        - platform Building Blocks
        - third Party Services
        - other University Services
        - secret Keys
    :return: True or False
    """
    if (not req_data['mobileAppVersion']) or (not req_data['platformBuildingBlocks']) or \
            (not req_data['thirdPartyServices']) or (not req_data['otherUniversityServices']) or \
            (not req_data['secretKeys']) or \
            (req_data['mobileAppVersion'] and (not dbutils.check_appversion_format(req_data['mobileAppVersion']))):
        return False
    return True


def decode(document):
    oid = document.pop('_id')
    if isinstance(oid, ObjectId):
        oid = str(oid)
    document['id'] = oid
    return document
