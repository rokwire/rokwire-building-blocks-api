import logging
import flask

# import sys
# sys.path.append('../')

from .db import get_db
from .config import LOGGING_COLL_NAME
from flask import Blueprint, request, make_response, abort, Flask

logging.basicConfig(format='%(asctime)-15s %(levelname)-7s [%(threadName)-10s] : %(name)s - %(message)s',
                    level=logging.INFO)
__logger = logging.getLogger("loggingservice")

bp = Blueprint('logging_rest_service', __name__, url_prefix='/logs')

@bp.route('/', methods=['POST'])
def post_events():
    try:
        in_json = request.get_json(force=True)

    except Exception as ex:
        __logger.exception(ex)
        abort(400)

    try:
        uuid = in_json["uuid"]
        db = get_db()

        # # for local test
        # from pymongo import MongoClient
        # client = MongoClient("mongodb://localhost:27017", connect=False)
        # db = client["loggingdb"]
        # LOGGING_COLL_NAME = "LogginDataset"

        object_id = db[LOGGING_COLL_NAME].insert(in_json)
        msg = "[POST]: logging record posted: uuid = %s" % str(uuid)
        __logger.info(msg)
    except Exception as ex:
        __logger.exception(ex)
        abort(500)
    return success_response(201, msg, str(uuid))


def success_response(status_code, msg, uuid):
    message = {
        'status': status_code,
        'uuid': uuid,
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
        'message': 'Log not found : ' + request.url,
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

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)