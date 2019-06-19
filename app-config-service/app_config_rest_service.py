import logging
import flask

from bson import ObjectId
from app_config_db import get_db
from flask import Blueprint, request, make_response, abort

logging.basicConfig(format='%(asctime)-15s %(levelname)-7s [%(threadName)-10s] : %(name)s - %(message)s',
                    level=logging.INFO)
__logger = logging.getLogger("app-config-service")

bp = Blueprint('app_config_rest_service', __name__, url_prefix='/app/configs')


@bp.route('/', methods=['GET'])
def get_app_configs():
    results = list()
    args = request.args
    query = dict()
    try:
        query = format_query(args, query)
    except Exception as ex:
        __logger.exception(ex)
        abort(500)
    if query:
        try:
            db = get_db()
            for data_tuple in db['appconfigs'].find(query):
                results.append(data_tuple)
        except Exception as ex:
            __logger.exception(ex)
            abort(500)

    msg = "[GET]: %s nRecords = %d " % (request.url, len(results))
    __logger.info(msg)
    return flask.jsonify(results)


@bp.route('/', methods=['POST'])
def post_app_config():
    req_data = request.get_json(force=True)

    try:
        db = get_db()
        app_config_id = db['appconfigs'].insert(req_data)
        msg = "[POST]: app config created: id = %s" % str(app_config_id)
        __logger.info(msg)
    except Exception as ex:
        __logger.exception(ex)
        abort(500)
    return success_response(201, msg, str(app_config_id))

@bp.route('/<id>', methods=['GET'])
def get_app_config_by_id(id):
    results = list()
    
    try:
        db = get_db()
        for data_tuple in db['appconfigs'].find({'_id': ObjectId(id)}):
            results.append(data_tuple)
    except Exception as ex:
        __logger.exception(ex)
        abort(500)

    msg = "[GET]: %s nRecords = %d " % (request.url, len(results))
    __logger.info(msg)
    return flask.jsonify(results)

@bp.route('/<id>', methods=['PUT'])
def update_app_config(id):
    if not ObjectId.is_valid(id):
        abort(400)
    req_data = request.get_json(force=True)

    try:
        db = get_db()
        status = db['appconfigs'].update_one({'_id': ObjectId(id)}, {"$set": req_data})
        msg = "[PUT]: app config id %s, nUpdate = %d " % (str(id), status.modified_count)
    except Exception as ex:
        __logger.exception(ex)
        abort(500)
    return success_response(200, msg, str(id))


@bp.route('/<id>', methods=['DELETE'])
def delete_app_config(id):
    if not ObjectId.is_valid(id):
        abort(400)
    try:
        db = get_db()
        status = db['appconfigs'].delete_one({'_id': ObjectId(id)})
        msg = "[DELETE]: app config id %s, nDelete = %d " % (str(id), status.deleted_count)
        __logger.info(msg)
    except Exception as ex:
        __logger.exception(ex)
        abort(500)

    return success_response(202, msg, str(id))


def success_response(status_code, msg, id):
    message = {
        'status': status_code,
        'id': id,
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
        'message': 'Events not found : ' + request.url,
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
        # app version query
        if args.get('mobileAppVersion'):
            query['$mobileAppVersion'] = {'$search': args.get('mobileAppVersion')}
        return query
