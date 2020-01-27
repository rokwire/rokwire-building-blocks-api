import logging
import re

import auth_middleware
import flask
import pymongo
from bson import ObjectId
from flask import request, make_response, abort, current_app
from pymongo.errors import DuplicateKeyError, CursorNotFound
from time import gmtime

from utils import db as conn
from utils.cache import memoize_query, CACHE_GET_APPCONFIG, CACHE_GET_APPCONFIGS
from utils import dbutils
import controllers.config as cfg

logging.Formatter.converter = gmtime
logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%dT%H:%M:%S',
                    format='%(asctime)-15s.%(msecs)03dZ %(levelname)-7s [%(threadName)-10s] : %(name)s - %(message)s')
__logger = logging.getLogger("app_config_building_block")
app = flask.Flask(__name__)


def configs_search(mobileAppVersion=None):
        args = request.args
        version = args.get('mobileAppVersion')
        query = dict()

        if version and dbutils.check_appversion_format(version) == False:
            abort(400)

        try:
            query = format_query(args, query)
        except Exception as ex:
            __logger.exception(ex)
            abort(500)
        try:
            result = _get_app_configs_result(query, version)

        except Exception as ex:
            __logger.exception(ex)
            abort(500)

        __logger.info("[GET]: %s nRecords = %d ", request.url, len(result))
        return flask.jsonify(result)


def configs_get(id):
    result = []
    if not ObjectId.is_valid(id):
        abort(400)
    try:
        result = _get_app_config_by_id_result({"_id": ObjectId(id)})
    except Exception as ex:
        __logger.exception(ex)
        abort(500)
    if len(result) == 0:
        abort(404)
    __logger.info("[GET]: %s nRecords = %d ", request.url, len(result))
    return flask.jsonify(result[0])


@memoize_query(**CACHE_GET_APPCONFIGS)
def _get_app_configs_result(query, version):
    """
        Perform the get_app_configs query and return a list of results. This is
        its own function to enable caching to work.
    """

    db = conn.get_db()
    cursor = db[cfg.APP_CONFIGS_COLLECTION].find(
        query,
        {"version_numbers": 0}
    ).sort([
        ("version_numbers.major", pymongo.DESCENDING),
        ("version_numbers.minor", pymongo.DESCENDING),
        ("version_numbers.patch", pymongo.DESCENDING)
    ])
    if version:
        cursor = cursor.limit(1)

    return [decode(c) for c in cursor]


@memoize_query(**CACHE_GET_APPCONFIG)
def _get_app_config_by_id_result(query):
    """
    Perform the get_app_config_by_id query and returns a list of results. This is
    its function to enable caching to work.
    Returns: a list of results
    """
    db = conn.get_db()
    cursor = db[cfg.APP_CONFIGS_COLLECTION].find(
        query,
        {"version_numbers": 0}
    )

    return [decode(c) for c in cursor]


def configs_post():
    req_data = request.get_json(force=True)
    if not check_format(req_data):
        abort(400)

    try:
        db = conn.get_db()
        add_version_numbers(req_data)
        app_config_id = db[cfg.APP_CONFIGS_COLLECTION].insert_one(req_data).inserted_id
        msg = "[POST]: api config document created: id = %s" % str(app_config_id)
        __logger.info(msg)

    except DuplicateKeyError as err:
        __logger.error(err)
        abort(400)

    except Exception as ex:
        __logger.exception(ex)
        abort(500)

    return success_response(201, msg, str(app_config_id))


def configs_put(id):
    req_data = request.get_json(force=True)
    if not check_format(req_data):
        abort(405)
    if not ObjectId.is_valid(id):
        abort(405)
    try:
        db = conn.get_db()
        add_version_numbers(req_data)
        status = db[cfg.APP_CONFIGS_COLLECTION].update_one({'_id': ObjectId(id)}, {"$set": req_data})
        msg = "[PUT]: api config id %s, nUpdate = %d " % (str(id), status.modified_count)

    except DuplicateKeyError as err:
        __logger.error(err)
        abort(405)

    except Exception as ex:
        __logger.exception(ex)
        abort(500)
    return success_response(200, msg, str(id))


def configs_delete(id):
    if not ObjectId.is_valid(id):
        abort(404)
    try:
        db = conn.get_db()
        status = db[cfg.APP_CONFIGS_COLLECTION].delete_one({'_id': ObjectId(id)})
        msg = "[DELETE]: api config id %s, nDelete = %d " % (str(id), status.deleted_count)
        __logger.info(msg)

    except Exception as ex:
        __logger.exception(ex)
        abort(500)

    return success_response(202, msg, str(id))


# =================================UTIL FUNCTIONS FOR REST SERVICES=====================================#
def success_response(status_code, msg, app_config_id):
    message = {
        'status': status_code,
        'id': app_config_id,
        'message': msg
    }
    resp = flask.jsonify(message)
    resp.status_code = status_code
    return make_response(resp)


@app.errorhandler(400)
def server_400_error(error=None):
    if error is None:
        error = {
            'error': 'Bad Request: ' + request.url,
        }
    resp = flask.jsonify(error)
    resp.status_code = 400
    return resp


@app.errorhandler(401)
def server_401_error(error=None):
    if error is None:
        error = {
            'message': 'Unauthorized : ' + request.url,
        }
    resp = flask.jsonify(error)
    resp.status_code = 401
    return resp


@app.errorhandler(404)
def server_404_error(error=None):
    if error is None:
        error = {
            'message': 'App config not found : ' + request.url + '. If search by mobile api version, please check the given version conforms major.minor.patch format, for example, 1.2.0',
        }
    resp = flask.jsonify(error)
    resp.status_code = 404
    return resp


@app.errorhandler(405)
def server_405_error(error=None):
    if error is None:
        error = {
            'message': 'Invalid input : ' + request.url,
        }
    resp = flask.jsonify(error)
    resp.status_code = 405
    return resp


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


def add_version_numbers(req_data):
    # to add a new mobile version into req_data db
    version = req_data['mobileAppVersion']
    version_numbers = dbutils.create_version_numbers(version)
    req_data['version_numbers'] = version_numbers


def check_format(req_data):
    if req_data['mobileAppVersion'] is None or req_data['platformBuildingBlocks'] is None or \
            req_data['thirdPartyServices'] is None or req_data['otherUniversityServices'] is None or \
            req_data['secretKeys'] is None or (req_data['mobileAppVersion'] and dbutils.check_appversion_format(req_data['mobileAppVersion']) is False):
        return False
    return True


def decode(document):
    oid = document.pop('_id')
    if isinstance(oid, ObjectId):
        oid = str(oid)
    document['id'] = oid
    return document
