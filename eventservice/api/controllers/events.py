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

import io
import os
import json
import logging
import flask
import flask.json
import auth_middleware
import pymongo

import requests

from bson import ObjectId
from flask import request, make_response, redirect, abort, current_app, g
from werkzeug.utils import secure_filename
from time import gmtime

import controllers.configs as cfg
from utils.db import get_db
from utils import query_params
from controllers.images.s3 import S3EventsImages
from controllers.images import localfile

from utils.cache import memoize , memoize_query, CACHE_GET_EVENTS, CACHE_GET_EVENT, CACHE_GET_EVENTIMAGES, CACHE_GET_CATEGORIES
from utils.group_auth import get_group_ids

logging.Formatter.converter = gmtime
logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%dT%H:%M:%S',
                    format='%(asctime)-15s.%(msecs)03dZ %(levelname)-7s [%(threadName)-10s] : %(name)s - %(message)s')
__logger = logging.getLogger("events_building_block")


def search():
    group_ids = list()
    include_private_events = False
    try:
        include_private_events, group_ids = get_group_ids()
    except Exception as ex:
        __logger.exception(ex)
        abort(500)

    args = request.args
    query = dict()
    try:
        query = query_params.format_query(args, query, include_private_events, group_ids)
    except Exception as ex:
        __logger.exception(ex)
        abort(400)
    try:
        result, result_len = _get_events_result(
            query,
            args.get('limit', 0, int),
            args.get('skip', 0, int)
        )
    except Exception as ex:
        __logger.exception(ex)
        abort(500)
    __logger.debug("[GET]: %s nRecords = %d ", request.url, result_len)
    return current_app.response_class(result, mimetype='application/json')


@memoize_query(**CACHE_GET_EVENTS)
def _get_events_result(query, limit, skip):
    """
    Perform the get_events query and return the serialized results. This is
    its own function to enable caching to work.
    Returns: (string, count)
    """
    if not query:
        return []

    is_super_event = False
    # public and private events query
    if query.get('$or'):
        for subquery in query.get('$or'):
            for cond in subquery.get('$and'):
                if cond.get('isSuperEvent'):
                    is_super_event = True
    # public events query
    else:
        for cond in query.get('$and'):
            if cond.get('isSuperEvent'):
                is_super_event = True

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
        # use the db `_id` as id in the returning event.
        event['id'] = str(event.pop('_id'))
        if is_super_event:
            subevents_ids = list()
            for subevent in event.get('subEvents'):
                subevents_ids.append(ObjectId(subevent.get("id")))
            # apply query to subevents
            params = query.get('$and')
            removed_params = list()
            for param in params:
                if param.get('_id'):
                    # remvoe super id query param
                    removed_params.append(param)
                elif param.get('isSuperEvent'):
                    # remove isSuperEvent query param
                    removed_params.append(param)
            for removed in removed_params:
                params.remove(removed)
            params.append({'_id': {'$in': subevents_ids}})

            subevents_cursor = db['events'].find(
                query,
                {'coordinates': 0, 'categorymainsub': 0}
            ).sort([
                ('startDate', pymongo.ASCENDING),
                ('endDate', pymongo.ASCENDING),
            ])
            for subevent_detail in subevents_cursor:
                subevent_detail['id'] = str(subevent_detail.pop('_id'))
                events.append(subevent_detail)
        else:
            events.append(event)
    return flask.json.dumps(events, default=query_params.format_datetime_response), len(events)


def tags_search():
    response = []
    try:
        tags_path = os.path.join(current_app.root_path, "tags.json")
        with open(tags_path, 'r') as tags_file:
            response = json.load(tags_file)
    except Exception as ex:
        __logger.exception(ex)
        abort(500)
    return flask.jsonify(response)


def super_events_tags_search():
    response = []
    try:
        tags_path = os.path.join(current_app.root_path, "superevents_tags.json")
        with open(tags_path, 'r') as tags_file:
            response = json.load(tags_file)
    except Exception as ex:
        __logger.exception(ex)
        abort(500)
    return flask.jsonify(response)


def categories_search():

    try:
        result, result_len = _get_categories_result()
    except Exception as ex:
        __logger.exception(ex)
        abort(500)

    __logger.debug("[GET]: %s nRecords = %d ", request.url, result_len)
    return current_app.response_class(result, mimetype='application/json')


@memoize(**CACHE_GET_CATEGORIES)
def _get_categories_result():
    """
    Perform the get_categories query and return the serialized results. This is
    its own function to enable caching to work.
    Returns: (string, count)
    """
    db = get_db()
    cursor = db['categories'].find(
        {},
        {'_id': 0}
    ).sort('category', pymongo.ASCENDING)

    categories = list(cursor)
    return flask.json.dumps(categories), len(categories)


def get(event_id):
    if not ObjectId.is_valid(event_id):
        abort(400)

    try:
        result, result_found = _get_event_result({'_id': ObjectId(event_id)})
    except Exception as ex:
        __logger.exception(ex)
        abort(500)

    if not result_found:
        abort(404)

    __logger.debug("[Get Event]: event id %s", event_id)
    return current_app.response_class(result, mimetype='application/json')


@memoize_query(**CACHE_GET_EVENT)
def _get_event_result(query):
    """
    Perform the get_event query and return the serialized results. This is
    its own function to enable caching to work.
    Returns: (string, found)
    """
    db = get_db()
    event = db['events'].find_one(
        query,
        {'_id': 0, 'coordinates': 0, 'categorymainsub': 0}
    )

    return flask.json.dumps(event, default=query_params.format_datetime_response), (not event is None)


def post():
    auth_middleware.authorize(auth_middleware.ROKWIRE_EVENT_WRITE_GROUPS)
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
        __logger.debug(msg)
    except Exception as ex:
        __logger.exception(ex)
        abort(500)
    return success_response(201, msg, str(event_id))


def put(event_id):
    auth_middleware.authorize(auth_middleware.ROKWIRE_EVENT_WRITE_GROUPS)

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
        status = db['events'].replace_one({'_id': ObjectId(event_id)}, req_data)
        msg = "[PUT]: event id %s, nUpdate = %d " % (str(event_id), status.modified_count)
    except Exception as ex:
        __logger.exception(ex)
        abort(500)
    return success_response(200, msg, str(event_id))


def patch(event_id):
    auth_middleware.authorize(auth_middleware.ROKWIRE_EVENT_WRITE_GROUPS)

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
        __logger.debug(msg)
    except Exception as ex:
        __logger.exception(ex)
        abort(500)
    return success_response(200, msg, str(event_id))


def delete(event_id):
    auth_middleware.authorize(auth_middleware.ROKWIRE_EVENT_WRITE_GROUPS)

    if not ObjectId.is_valid(event_id):
        abort(400)
    try:
        db = get_db()
        status = db['events'].delete_one({'_id': ObjectId(event_id)})
        msg = "[DELETE]: event id %s, nDelete = %d " % (str(event_id), status.deleted_count)
        __logger.debug(msg)
    except Exception as ex:
        __logger.exception(ex)
        abort(500)
    if status.deleted_count == 0:
        abort(404)
    return success_response(202, msg, str(event_id))


def images_search(event_id):
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
    cursor = db[cfg.IMAGE_COLLECTION].find(
        query,
        {'_id': 1}
    )

    return [str(i['_id']) for i in cursor]


def images_post(event_id):
    auth_middleware.authorize(auth_middleware.ROKWIRE_EVENT_WRITE_GROUPS)

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
                result = db[cfg.IMAGE_COLLECTION].insert_one({
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


def images_get(event_id, image_id):
    # TODO: add in again when the client starts sending the API key for this
    # endpoint
    if not ObjectId.is_valid(event_id) or not ObjectId.is_valid(image_id):
        abort(400)

    url = cfg.IMAGE_URL.format(
        bucket=cfg.BUCKET,
        region=os.getenv('AWS_DEFAULT_REGION'),
        prefix=cfg.AWS_IMAGE_FOLDER_PREFIX,
        event_id=event_id,
        image_id=image_id,
    )
    __logger.debug("[download image] redirect to %s", url)
    return redirect(url, code=302)


def images_put(event_id, image_id):
    auth_middleware.authorize(auth_middleware.ROKWIRE_EVENT_WRITE_GROUPS)

    tmpfile = None
    try:
        db = get_db()
        # check if image exists
        if db[cfg.IMAGE_COLLECTION].find_one({'_id': ObjectId(image_id)}):
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


def images_delete(event_id, image_id):
    auth_middleware.authorize(auth_middleware.ROKWIRE_EVENT_WRITE_GROUPS)

    msg = "[delete image]: event id %s, image id: %s" % (str(event_id), str(image_id))
    try:
        S3EventsImages().delete(event_id, image_id)
        db = get_db()
        db[cfg.IMAGE_COLLECTION].delete_one({
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
