import logging
import json
import sys

from connexion.exceptions import OAuthProblem

# from models.config import LOGGING_URL_PREFIX #, LOGGING_COLL_NAME
from flask import request

import utils.rest_handlers as rs_handlers

def post():
    in_json = None
    try:
        in_json = request.get_json(force=True)
        if not isinstance(in_json, list):
            msg = "request json is not a list"
            logging.info(msg)
            return rs_handlers.server_400_error(msg)
    except Exception as ex:
        logging.exception(ex)
        raise OAuthProblem(ex)

    try:
        # db = get_db()

        # # for local test
        # from pymongo import MongoClient
        # client = MongoClient("mongodb://localhost:27017", connect=False)
        # db = client["loggingdb"]
        # LOGGING_COLL_NAME = "logs"

        # Insert log entries to database.
        if in_json is not None:
            # db[LOGGING_COLL_NAME].insert_many(in_json)

            # Write incoming click stream data to log (for easy integration with Splunk)
            for log in in_json:
                print(json.dumps(log))
            sys.stdout.flush()

    except Exception as ex:
        logging.exception(ex)
        raise OAuthProblem(ex)

    return rs_handlers.success_response_only_status_code(200, "logging information successfully posted")