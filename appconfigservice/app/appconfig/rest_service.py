import logging
import flask
import re

from bson import ObjectId
from appconfig import db as conn
from appconfig import dbutils 
from flask import Blueprint, request, make_response, abort, current_app
from pymongo.errors import DuplicateKeyError
import pymongo

logging.basicConfig(format='%(asctime)-15s %(levelname)-7s [%(threadName)-10s] : %(name)s - %(message)s',
                    level=logging.INFO)
__logger = logging.getLogger("app_config_service")

bp = Blueprint('app_config_rest_service', __name__, url_prefix='/app/configs')

@bp.route('/', methods=['GET'])
def get_app_configs():
    results = list()
    args = request.args
    query = dict()
    version = args.get('mobileAppVersion')
    if version and dbutils.check_appversion_format(version) == False:
        abort(404)
    try:
        query = format_query(args, query)
    except Exception as ex:
        __logger.exception(ex)
        abort(500)
    try:
        db = conn.get_db()
        if version:
            for document in db[current_app.config['APP_CONFIGS_COLLECTION']].find(query).sort([("mobileAppVersion", pymongo.DESCENDING)]).limit(1):
                config = decode(document)
                results.append(config)
        else:
            for document in db[current_app.config['APP_CONFIGS_COLLECTION']].find(query).sort([("mobileAppVersion", pymongo.DESCENDING)]):
                config = decode(document)
                results.append(config)
    except Exception as ex:
            __logger.exception(ex)
            abort(500)
    msg = "[GET]: %s nRecords = %d " % (request.url, len(results))
    __logger.info(msg)
    return flask.jsonify(results)

@bp.route('/<id>', methods=['GET'])
def get_app_config_by_id(id):
    results = list()
    if not ObjectId.is_valid(id):
        abort(400)
    try:
        db = conn.get_db()
        for document in db[current_app.config['APP_CONFIGS_COLLECTION']].find({"_id": ObjectId(id)}):
            config = decode(document)
            results.append(config)
    except Exception as ex:
            __logger.exception(ex)
            abort(500)
    msg = "[GET]: %s nRecords = %d " % (request.url, len(results))
    __logger.info(msg)
    return flask.jsonify(results)

@bp.route('/', methods=['POST'])
def post_app_config():
    req_data = request.get_json(force=True)
    if not check_format(req_data):
        abort(400)
    try:
        db = conn.get_db()
        app_config_id = db[current_app.config['APP_CONFIGS_COLLECTION']].insert_one(req_data).inserted_id
        msg = "[POST]: app config document created: id = %s" % str(app_config_id)
        __logger.info(msg)
    except DuplicateKeyError as err:
        __logger.error(err)
        abort(500)
    except Exception as ex:
        __logger.exception(ex)
        abort(500)
    return success_response(201, msg, str(app_config_id))


@bp.route('/<id>', methods=['PUT'])
def update_app_config(id):
    if not ObjectId.is_valid(id):
        abort(400)
    req_data = request.get_json(force=True)
    if not check_format(req_data):
        abort(400)
    try:
        db = conn.get_db()
        status = db[current_app.config['APP_CONFIGS_COLLECTION']].update_one({'_id': ObjectId(id)}, {"$set": req_data})
        msg = "[PUT]: app config id %s, nUpdate = %d " % (str(id), status.modified_count)
    except DuplicateKeyError as err:
        __logger.error(err)
        abort(500)
    except Exception as ex:
        __logger.exception(ex)
        abort(500)
    return success_response(200, msg, str(id))

@bp.route('/<id>', methods=['DELETE'])
def delete_app_config(id):
    if not ObjectId.is_valid(id):
        abort(400)
    try:
        db = conn.get_db()
        status = db[current_app.config['APP_CONFIGS_COLLECTION']].delete_one({'_id': ObjectId(id)})
        msg = "[DELETE]: app config id %s, nDelete = %d " % (str(id), status.deleted_count)
        __logger.info(msg)
    except Exception as ex:
        __logger.exception(ex)
        abort(500)
    return success_response(202, msg, str(id))


def success_response(status_code, msg, app_config_id):
    message = {
        'status': status_code,
        'id': app_config_id,
        'message': msg
    }
    resp = flask.jsonify(message)
    resp.status_code = status_code
    return make_response(resp)


@bp.errorhandler(400)
def server_400_error(error=None):
    message = {
        'status': 400,
        'message': 'Bad request : ' + request.url,
    }
    resp = flask.jsonify(message)
    resp.status_code = 400
    return resp


@bp.errorhandler(401)
def server_401_error(error=None):
    message = {
        'status': 401,
        'message': 'Unauthorized : ' + request.url,
    }
    resp = flask.jsonify(message)
    resp.status_code = 401
    return resp


@bp.errorhandler(404)
def server_404_error(error=None):
    message = {
        'status': 404,
        'message': 'App config not found : ' + request.url + '. If search by mobile app version, please check the given version conforms major.minor.patch format, for example, 1.2.0',
    }
    resp = flask.jsonify(message)
    resp.status_code = 404
    return resp


@bp.errorhandler(405)
def server_405_error(error=None):
    message = {
        'status': 405,
        'message': 'Invalid input : ' + request.url,
    }
    resp = flask.jsonify(message)
    resp.status_code = 405
    return resp

@bp.errorhandler(500)
def server_500_error(error=None):
    message = {
        'status': 500,
        'message': 'Internal error : ' + request.url,
    }
    resp = flask.jsonify(message)
    resp.status_code = 500
    return resp

def format_query(args, query):
    version = args.get('mobileAppVersion')
    if version is not None and dbutils.check_appversion_format(version):
        #m = re.match(dbutils.VERSION_NUMBER_REGX, version)
        #query = {'$or': [
        #    {'version_numbers.major': {'$lt' : int(m.group(1))}},
        #    {'$and': [{'version_numbers.major': {'$eq': int(m.group(1))}}, {'version_numbers.minor': {'$lt': int(m.group(2))}}]},
        #    {'$and': [{'version_numbers.major': {'$eq': int(m.group(1))}}, {'version_numbers.minor': {'$eq': int(m.group(2))}}, {'version_numbers.patch': {'$lte': int(m.group(3))}}]}
        #]}
        query = {'mobileAppVersion': {'$lte': version}}
    return query
    
def check_format(req_data):
    if req_data['mobileAppVersion'] is None or req_data['platformBuildingBlocks'] is None or \
            req_data['thirdPartyServices'] is None or req_data['otherUniversityServices'] is None or \
            req_data['secretKeys'] is None or (req_data['mobileAppVersion'] and dbutils.check_appversion_format(req_data['mobileAppVersion']) is False):
        return False
    return True
    
def decode(document):
    dto = {}
    oid = document['_id']
    if isinstance(oid, ObjectId):
        oid = str(oid)
    dto['id'] = oid
    dto['mobileAppVersion'] = document['mobileAppVersion']
    dto['platformBuildingBlocks'] = document['platformBuildingBlocks']
    dto['thirdPartyServices'] = document['thirdPartyServices']
    dto['otherUniversityServices'] = document['otherUniversityServices']
    if 'secretKeys' in document.keys():
        dto['secretKeys'] = document['secretKeys']
    return dto
    