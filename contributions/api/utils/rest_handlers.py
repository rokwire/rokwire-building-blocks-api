#  Copyright 2020 Board of Trustees of the University of Illinois.

import flask
from flask import flash, redirect, jsonify, make_response, request


app = flask.Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

"""
make reponse for handling 202 entry deleted
"""

def return_id(msg, idfield, id):
    message = {
        idfield: id,
        'message': msg,
    }
    resp = jsonify(message)
    resp.status_code = 200

    return make_response(resp)

def entry_deleted(id_type, id):
    message = {
        id_type: id
    }
    resp = jsonify(message)
    resp.status_code = 202

    return make_response(resp)

@app.errorhandler(400)
def bad_request(error=None):
    if error is None:
        error = {
            'error': 'Bad Request: ' + request.url,
        }
    resp = jsonify(error)
    resp.status_code = 400

    return resp

@app.errorhandler(403)
def forbidden(error=None):
    if error is None:
        error = {
            'error': 'Forbidden: ' + request.url,
        }
    resp = jsonify(error)
    resp.status_code = 403

    return resp

@app.errorhandler(404)
def not_found(error=None):
    if error is None:
        error = {'error': 'Not Found: ' + request.url}
    resp = jsonify(error)
    resp.status_code = 404

    return resp

@app.errorhandler(415)
def unsupported_media_type(error=None):
    if error is None:
        error = {
            'error': 'Unsupported media type: ' + request.url,
        }
    resp = jsonify(error)
    resp.status_code = 415

    return resp

@app.errorhandler(500)
def internal_server_error(error=None):
    if error is None:
        error = {
            'error': 'Internal Server Error: ' + request.url,
        }
    resp = jsonify(error)
    resp.status_code = 500

    return resp

@app.errorhandler(501)
def not_implemented(error=None):
    if error is None:
        error = {
            'error': 'Not Implemented: ' + request.url,
        }
    resp = jsonify(error)
    resp.status_code = 501

    return resp
