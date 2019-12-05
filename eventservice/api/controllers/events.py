import io
import os
import json
import logging
import flask
import flask.json
import auth_middleware
import pymongo

from bson import ObjectId


from bson import ObjectId
from utils.db import get_db
from utils import query_params
from controllers.configs import URL_PREFIX
from controllers.images.s3 import S3EventsImages
from controllers.images import localfile
from flask import Blueprint, request, make_response, redirect, abort, current_app
from werkzeug.utils import secure_filename
from time import gmtime
from utils.cache import memoize , memoize_query, CACHE_GET_EVENTS, CACHE_GET_EVENT, CACHE_GET_EVENTIMAGES, CACHE_GET_CATEGORIES
#
logging.Formatter.converter = gmtime
logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%dT%H:%M:%S',
                    format='%(asctime)-15s.%(msecs)03dZ %(levelname)-7s [%(threadName)-10s] : %(name)s - %(message)s')
__logger = logging.getLogger("events_building_block")


def search():
    # auth_middleware.verify_secret(request)
    args = request.args
    query = dict()
    try:
        query = query_params.format_query(args, query)
    except Exception as ex:
        __logger.exception(ex)
        abort(500)
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
    return flask.json.dumps(events), len(events)


def tags_search():
    # auth_middleware.verify_secret(request)
    response = []
    try:
        tags_path = os.path.join(current_app.root_path, "tags.json")
        with open(tags_path, 'r') as tags_file:
            response = json.load(tags_file)
    except Exception as ex:
        __logger.exception(ex)
        abort(500)
    return flask.jsonify(response)


def categories_search():
    # auth_middleware.verify_secret(request)

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
