import io
import os
import json
import logging
import flask
import auth_middleware
import pymongo

from bson import ObjectId
from .db import get_db
from . import query_params
from .config import URL_PREFIX
from .images.s3 import S3EventsImages
from .images import localfile
from flask import Blueprint, request, make_response, redirect, abort, current_app
from werkzeug.utils import secure_filename
from time import gmtime
from .cache import memoize, memoize_query, CACHE_GET_EVENTS, CACHE_GET_EVENT, CACHE_GET_EVENTIMAGES, CACHE_GET_CATEGORIES

logging.Formatter.converter = gmtime
logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%dT%H:%M:%S',
                    format='%(asctime)-15s.%(msecs)03dZ %(levelname)-7s [%(threadName)-10s] : %(name)s - %(message)s')
__logger = logging.getLogger("events_building_block")

bp = Blueprint('event_rest_service', __name__, url_prefix=URL_PREFIX)


# A couple of proposed groups


@bp.route('/tags', methods=['GET'])
def get_tags():
    auth_middleware.verify_secret(request)
    response = []
    try:
        tags_path = os.path.join(current_app.root_path, "tags.json")
        with open(tags_path, 'r') as tags_file:
            response = json.load(tags_file)
    except Exception as ex:
        __logger.exception(ex)
        abort(500)
    return flask.jsonify(response)


@bp.route('/categories', methods=['GET'])
def get_categories():
    auth_middleware.verify_secret(request)

    try:
        result = _get_categories_result()
    except Exception as ex:
        __logger.exception(ex)
        abort(500)

    __logger.info("[GET]: %s nRecords = %d ", request.url, len(result))
    return flask.jsonify(result)

@memoize(**CACHE_GET_CATEGORIES)
def _get_categories_result():
    """
    Perform the get_categories query and return the results. This is
    its own function to enable caching to work.

    Returns: result
    """
    db = get_db()
    cursor = db['categories'].find(
        {},
        {'_id': 0}
    ).sort('category', pymongo.ASCENDING)

    return list(cursor)


@bp.route('/', methods=['GET'])
def get_events():
    auth_middleware.verify_secret(request)
    args = request.args
    query = dict()
    try:
        query = query_params.format_query(args, query)
    except Exception as ex:
        __logger.exception(ex)
        abort(500)

    try:
        result = _get_events_result(
            query,
            args.get('limit', 0, int),
            args.get('skip', 0, int)
        )
    except Exception as ex:
        __logger.exception(ex)
        abort(500)

    __logger.info("[GET]: %s nRecords = %d ", request.url, len(result))
    return flask.jsonify(result)

@memoize_query(**CACHE_GET_EVENTS)
def _get_events_result(query, limit, skip):
    """
    Perform the get_events query and return the results. This is
    its own function to enable caching to work.

    Returns: result
    """
    if not query:
        return []

    db = get_db()
    cursor = db['events'].find(
        query,
        {'coordinates': 0, 'categorymainsub': 0}
    ).sort([
        ('startDate', pymongo.ASCENDING),
        ('endDate', pymongo.ASCENDING),
    ])
    if limit > 0:
        cursor = cursor.limit(limit)
    if skip > 0:
        cursor = cursor.skip(skip)

    events = []
    for event in cursor:
        event['id'] = str(event.pop('_id'))
        events.append(event)
    return events


@bp.route('/', methods=['POST'])
def post_events():
    auth_middleware.authenticate(auth_middleware.rokwire_event_manager_group)
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
    auth_middleware.authenticate(auth_middleware.rokwire_event_manager_group)


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
    auth_middleware.authenticate(auth_middleware.rokwire_event_manager_group)

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


@bp.route('/<event_id>', methods=['GET'])
def get_event(event_id):
    auth_middleware.verify_secret(request)

    if not ObjectId.is_valid(event_id):
        abort(400)

    try:
        result = _get_event_result({'_id': ObjectId(event_id)})
    except Exception as ex:
        __logger.exception(ex)
        abort(500)

    if not result:
        abort(404)

    __logger.info("[Get Event]: event id %s", event_id)
    return flask.jsonify(result)

@memoize_query(**CACHE_GET_EVENT)
def _get_event_result(query):
    """
    Perform the get_event query and return the results. This is
    its own function to enable caching to work.

    Returns: result
    """
    db = get_db()
    event = db['events'].find_one(
        query,
        {'_id': 0, 'coordinates': 0, 'categorymainsub': 0}
    )

    return event


@bp.route('/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    auth_middleware.authenticate(auth_middleware.rokwire_event_manager_group)

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


@bp.route('/<event_id>/images/<image_id>', methods=['GET'])
def download_imagefile(event_id, image_id):
    auth_middleware.verify_secret(request)

    if not ObjectId.is_valid(event_id) or not ObjectId.is_valid(image_id):
        abort(400)

    url = current_app.config['IMAGE_URL'].format(
        bucket=current_app.config['BUCKET'],
        region=os.getenv('AWS_DEFAULT_REGION'),
        prefix=current_app.config['AWS_IMAGE_FOLDER_PREFIX'],
        event_id=event_id,
        image_id=image_id,
    )
    __logger.info("[download image] redirect to %s", url)
    return redirect(url, code=302)


@bp.route('/<event_id>/images/<image_id>', methods=['PUT'])
def put_imagefile(event_id, image_id):
    auth_middleware.authenticate(auth_middleware.rokwire_event_manager_group)

    tmpfile = None
    try:
        db = get_db()
        # check if image exists
        if db[current_app.config['IMAGE_COLLECTION']].find_one({'_id': ObjectId(image_id)}):
            file = request.files.get('file')
            if file:
                if file.filename == '':
                    raise
                if localfile.allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    tmpfile = localfile.savefile(file, filename)
                    S3EventsImages().upload(tmpfile, event_id, image_id)
                    msg = "[put image]: image id %s" % (str(image_id))
                else:
                    raise
            else:
                raise
        else:
            raise
    except Exception as ex:
        __logger.exception(ex)
        abort(500)
    finally:
        localfile.deletefile(tmpfile)

    return success_response(200, msg, str(image_id))


@bp.route('/<event_id>/images', methods=['GET'])
def get_imagefiles(event_id):
    auth_middleware.verify_secret(request)

    if not ObjectId.is_valid(event_id):
        abort(400)

    try:
        result = _get_imagefiles_result({'eventId': event_id})
    except Exception as ex:
        __logger.exception(ex)
        abort(500)

    msg = "[get images]: find %d images related to event %s" % (len(result), event_id)
    return success_response(200, msg, result)

@memoize_query(**CACHE_GET_EVENTIMAGES)
def _get_imagefiles_result(query):
    """
    Perform the get_imagefiles query and return the results. This is
    its own function to enable caching to work.

    Returns: result
    """
    db = get_db()
    cursor = db[current_app.config['IMAGE_COLLECTION']].find(
        query,
        {'_id': 1}
    )

    return [str(i['_id']) for i in cursor]


@bp.route('/<event_id>/images', methods=['POST'])
def post_imagefile(event_id):
    auth_middleware.authenticate(auth_middleware.rokwire_event_manager_group)

    tmpfile = None
    try:
        file = request.files.get('file')
        if file:
            if file.filename == '':
                raise
            if localfile.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                tmpfile = localfile.savefile(file, filename)
                db = get_db()
                result = db[current_app.config['IMAGE_COLLECTION']].insert_one({
                    'eventId': event_id
                })
                image_id = str(result.inserted_id)
                S3EventsImages().upload(tmpfile, event_id, image_id)
                msg = "[post image]: image id %s" % (str(image_id))
            else:
                raise
        else:
            raise
    except Exception as ex:
        __logger.exception(ex)
        abort(500)
    finally:
        localfile.deletefile(tmpfile)
    return success_response(201, msg, str(image_id))


@bp.route('/<event_id>/images/<image_id>', methods=['DELETE'])
def delete_imagefile(event_id, image_id):
    auth_middleware.authenticate(auth_middleware.rokwire_event_manager_group)

    msg = "[delete image]: event id %s, image id: %s" % (str(event_id), str(image_id))
    try:
        S3EventsImages().delete(event_id, image_id)
        db = get_db()
        db[current_app.config['IMAGE_COLLECTION']].delete_one({
            '_id': ObjectId(image_id)
        })
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
