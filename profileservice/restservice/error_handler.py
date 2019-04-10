from flask import request, jsonify
from profileservice.restservice.rest_service import app

"""
error handlers
"""



@app.errorhandler(400)
def bad_request(error=None):
    message = {
            'status': 400,
            'message': 'Bad Request: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 400

    return resp

@app.errorhandler(403)
def forbidden(error=None):
    message = {
            'status': 403,
            'message': 'Forbidden: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 403

    return resp

@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.errorhandler(415)
def unsupported_media_type(error=None):
    message = {
            'status': 415,
            'message': 'Unsupported media type: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 415

    return resp