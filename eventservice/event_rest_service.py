import logging
import flask
import datetime

from pymongo.mongo_client import MongoClient
from bson import ObjectId

from flask import request, current_app, make_response, abort

app = flask.Flask(__name__)
app.config.from_pyfile('config.py', silent=True)
logging.basicConfig(format='%(asctime)-15s %(levelname)-7s [%(threadName)-10s] : %(name)s - %(message)s',
                    level=logging.INFO)
__logger = logging.getLogger("eventservice")


@app.route('/events', methods=['GET'])
def get_events():
    results = dict()
    args = request.args
    query = dict()
    # title text query
    if args.get('title'):
        query['$text'] = {'$search': args.get('title')}
    # tags query
    if args.getlist('tags'):
        query['tags'] = {'$all': args.getlist('tags')}
    # target audience query
    if args.get('targetAudience'):
        query['targetAudience'] = {'$in': args.getlist('targetAudience')}
    # datetime range query
    if args.get('startDate'):
        query['startDate'] = {'$gte': datetime.datetime.strptime(args.get('startDate'), "%Y-%m-%dT%H:%M:%S")}
    if args.get('endDate'):
        query['endDate'] = {'$lte': datetime.datetime.strptime(args.get('endDate'), "%Y-%m-%dT%H:%M:%S")}
    # geolocation query
    if args.get('latitude') and args.get('longitude') and args.get('radius'):
        coordinates = [float(args.get('longitude')), float(args.get('latitude'))]
        radius_meters = int(args.get('radius'))
        query['coordinates'] = {'$geoWithin': {'$centerSphere': [coordinates, radius_meters*0.000621371/3963.2]}}

    count = 0
    if query:
        try:
            with MongoClient(current_app.config['EVENT_MONGO_URL'], connect=False) as mongo:
                db = mongo.get_database(current_app.config['EVENT_DB_NAME'])
                for data_tuple in db['events'].find(query, {'_id': 0, 'coordinates': 0}):
                    count += 1
                    results["event"+str(count)] = data_tuple
        except Exception as ex:
            __logger.exception(ex)
            abort(500)

        if count == 0:
            abort(404)
    msg = "[GET]: %s nRecords = %d " % (request.url, count)
    __logger.info(msg)
    return flask.jsonify(results)


@app.route('/events', methods=['POST'])
def post_events():
    req_data = request.get_json(force=True)
    try:
        start_date = req_data.get('startDate')
        req_data['startDate'] = datetime.datetime.strptime(start_date, "%Y/%m/%dT%H:%M:%S")
        end_date = req_data.get('endDate')
        req_data['endDate'] = datetime.datetime.strptime(end_date, "%Y/%m/%dT%H:%M:%S")
    except Exception as ex:
        __logger.exception(ex)
        abort(400)

    if req_data['startDate'] is None or req_data['endDate'] is None or req_data['eventType'] is None or \
            req_data['sponsor'] is None or req_data['title'] is None:
        abort(400)

    if req_data.get('location'):
        location = req_data.get('location')
        if location.get('longitude') and location.get('latitude'):
            req_data['coordinates'] = [location.get('longitude'), location.get('latitude')]
    try:
        with MongoClient(current_app.config['EVENT_MONGO_URL'], connect=False) as mongo:
            db = mongo.get_database(current_app.config['EVENT_DB_NAME'])
            event_id = db['events'].insert(req_data)
            msg = "[POST]: event record created: id = %s" % str(event_id)
            __logger.info(msg)
    except Exception as ex:
        __logger.exception(ex)
        abort(500)
    return success_response(201, msg, str(event_id))


@app.route('/events/<event_id>', methods=['PUT'])
def update_event(event_id):
    if not ObjectId.is_valid(event_id):
        abort(400)
    req_data = request.get_json(force=True)
    try:
        with MongoClient(current_app.config['EVENT_MONGO_URL'], connect=False) as mongo:
            db = mongo.get_database(current_app.config['EVENT_DB_NAME'])
            status = db['events'].update_one({'_id': ObjectId(event_id)}, {"$set": req_data})
            msg = "[PUT]: event id %s, nUpdate = %d " % (str(event_id), status.modified_count)
    except Exception as ex:
        __logger.exception(ex)
        abort(500)
    return success_response(200, msg, str(event_id))


@app.route('/events/<event_id>', methods=['PATCH'])
def partial_update_event(event_id):
    if not ObjectId.is_valid(event_id):
        abort(400)
    req_data = request.get_json(force=True)
    try:
        if req_data.get('startDate'):
            start_date = req_data.get('startDate')
            req_data['startDate'] = datetime.datetime.strptime(start_date, "%Y/%m/%dT%H:%M:%S")

        if req_data.get('endDate'):
            end_date = req_data.get('endDate')
            req_data['endDate'] = datetime.datetime.strptime(end_date, "%Y/%m/%dT%H:%M:%S")

        coordinates = []
        try:
            if req_data.get('location.latitude') or req_data.get('location.latitude'):
                with MongoClient(current_app.config['EVENT_MONGO_URL'], connect=False) as mongo:
                    db = mongo.get_database(current_app.config['EVENT_DB_NAME'])
                    for data_tuple in db['events'].find({'_id': ObjectId(event_id)}, {'_id': 0, 'coordinates': 1}):
                        coordinates = data_tuple.get('coordinates')
                        if not coordinates:
                            abort(500)
                        break
        except Exception as ex:
            __logger.exception(ex)
            abort(500)

        if req_data.get('location.latitude'):
            coordinates[1] = req_data.get('location.latitude')
            req_data['coordinates'] = coordinates

        if req_data.get('location.longitude'):
            coordinates[0] = req_data.get('location.longitude')
            req_data['coordinates'] = coordinates
    except Exception as ex:
        __logger.exception(ex)
        abort(405)

    try:
        with MongoClient(current_app.config['EVENT_MONGO_URL'], connect=False) as mongo:
            db = mongo.get_database(current_app.config['EVENT_DB_NAME'])
            status = db['events'].update_one({'_id': ObjectId(event_id)}, {"$set": req_data})
            msg = "[PATCH]: event id %s, nUpdate = %d " % (str(event_id), status.modified_count)
            __logger.info(msg)
    except Exception as ex:
        __logger.exception(ex)
        abort(500)
    return success_response(200, msg, str(event_id))


@app.route('/events/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    if not ObjectId.is_valid(event_id):
        abort(400)
    try:
        with MongoClient(current_app.config['EVENT_MONGO_URL'], connect=False) as mongo:
            db = mongo.get_database(current_app.config['EVENT_DB_NAME'])
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


@app.errorhandler(400)
def server_400_error(error=None):
    message = {
        'status': 400,
        'message': 'Bad request : ' + request.url,
    }
    resp = flask.jsonify(message)
    resp.status_code = 400
    return resp


@app.errorhandler(401)
def server_401_error(error=None):
    message = {
        'status': 401,
        'message': 'Unauthorized : ' + request.url,
    }
    resp = flask.jsonify(message)
    resp.status_code = 401
    return resp


@app.errorhandler(404)
def server_404_error(error=None):
    message = {
        'status': 404,
        'message': 'Events not found : ' + request.url,
    }
    resp = flask.jsonify(message)
    resp.status_code = 404
    return resp


@app.errorhandler(405)
def server_405_error(error=None):
    message = {
        'status': 405,
        'message': 'Invalid input : ' + request.url,
    }
    resp = flask.jsonify(message)
    resp.status_code = 405
    return resp


@app.errorhandler(500)
def server_500_error(error=None):
    message = {
        'status': 500,
        'message': 'Internal error : ' + request.url,
    }
    resp = flask.jsonify(message)
    resp.status_code = 500
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
