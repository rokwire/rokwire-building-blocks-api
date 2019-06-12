import logging
import flask

from bson import ObjectId
from .db import get_db
from . import query_params
from flask import Blueprint, request, make_response, abort

logging.basicConfig(format='%(asctime)-15s %(levelname)-7s [%(threadName)-10s] : %(name)s - %(message)s',
                    level=logging.INFO)
__logger = logging.getLogger("eventservice")

bp = Blueprint('event_rest_service', __name__, url_prefix='/events')


@bp.route('/categories', methods=['GET'])
def get_categories():
    results = list()
    try:
        db = get_db()
        for data_tuple in db['categories'].find({}, {'_id': 0}):
            results.append(data_tuple)
    except Exception as ex:
        __logger.exception(ex)
        abort(500)
    msg = "[GET]: %s nRecords = %d " % (request.url, len(results))
    __logger.info(msg)
    return flask.jsonify(results)


@bp.route('/', methods=['GET'])
def get_events():
    results = list()
    args = request.args
    query = dict()
    try:
        query = query_params.format_query(args, query)
    except Exception as ex:
        __logger.exception(ex)
        abort(500)
    if query:
        try:
            db = get_db()
            for data_tuple in db['events'].find(query, {'_id': 0, 'coordinates': 0, 'categorymainsub': 0}):
                results.append(data_tuple)
        except Exception as ex:
            __logger.exception(ex)
            abort(500)

    msg = "[GET]: %s nRecords = %d " % (request.url, len(results))
    __logger.info(msg)
    return flask.jsonify(results)


@bp.route('/', methods=['POST'])
def post_events():
    req_data = request.get_json(force=True)

    if not query_params.required_check(req_data):
        abort(400)
    try:
        req_data = query_params.formate_datetime(req_data)
        req_data = query_params.formate_location(req_data)
        req_data = query_params.formate_category(req_data)
    except Exception as ex:
        __logger.exception(ex)
        abort(400)

    try:
        db = get_db()
        event_id = db['events'].insert(req_data)
        msg = "[POST]: event record created: id = %s" % str(event_id)
        __logger.info(msg)
    except Exception as ex:
        __logger.exception(ex)
        abort(500)
    return success_response(201, msg, str(event_id))


@bp.route('/<event_id>', methods=['PUT'])
def update_event(event_id):
    if not ObjectId.is_valid(event_id):
        abort(400)
    req_data = request.get_json(force=True)

    if not query_params.required_check(req_data):
        abort(400)
    try:
        req_data = query_params.formate_datetime(req_data)
        req_data = query_params.formate_location(req_data)
        req_data = query_params.formate_category(req_data)
    except Exception as ex:
        __logger.exception(ex)
        abort(400)

    try:
        db = get_db()
        status = db['events'].update_one({'_id': ObjectId(event_id)}, {"$set": req_data})
        msg = "[PUT]: event id %s, nUpdate = %d " % (str(event_id), status.modified_count)
    except Exception as ex:
        __logger.exception(ex)
        abort(500)
    return success_response(200, msg, str(event_id))


@bp.route('/<event_id>', methods=['PATCH'])
def partial_update_event(event_id):
    if not ObjectId.is_valid(event_id):
        abort(400)
    req_data = request.get_json(force=True)
    try:
        req_data = query_params.formate_datetime(req_data)
        if req_data.get('category') or req_data.get('subcategory'):
            db = get_db()
            for data_tuple in db['events'].find({'_id': ObjectId(event_id)}, {'_id': 0, 'categorymainsub': 1}):
                req_data = query_params.update_category(req_data, data_tuple)
                break

        coordinates = []
        try:
            if req_data.get('location.latitude') or req_data.get('location.latitude'):
                db = get_db()
                for data_tuple in db['events'].find({'_id': ObjectId(event_id)}, {'_id': 0, 'coordinates': 1}):
                    coordinates = data_tuple.get('coordinates')
                    if not coordinates:
                        abort(500)
                    break
                req_data = query_params.update_coordinates(req_data, coordinates)
        except Exception as ex:
            __logger.exception(ex)
            abort(500)

    except Exception as ex:
        __logger.exception(ex)
        abort(405)

    try:
        db = get_db()
        status = db['events'].update_one({'_id': ObjectId(event_id)}, {"$set": req_data})
        msg = "[PATCH]: event id %s, nUpdate = %d " % (str(event_id), status.modified_count)
        __logger.info(msg)
    except Exception as ex:
        __logger.exception(ex)
        abort(500)
    return success_response(200, msg, str(event_id))


@bp.route('/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    if not ObjectId.is_valid(event_id):
        abort(400)
    try:
        db = get_db()
        status = db['events'].delete_one({'_id': ObjectId(event_id)})
        msg = "[DELETE]: event id %s, nDelete = %d " % (str(event_id), status.deleted_count)
        __logger.info(msg)
    except Exception as ex:
        __logger.exception(ex)
        abort(500)

    return success_response(202, msg, str(event_id))


def success_response(status_code, msg, event_id):
    message = {
        'status': status_code,
        'id': event_id,
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
