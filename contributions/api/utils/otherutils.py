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

import uuid
import json
import datetime
import logging

from flask import jsonify, request, g
from bson import ObjectId

import controllers.configs as cfg
import utils.jsonutils as jsonutils
import utils.rest_handlers as rs_handlers
import utils.mongoutils as mongoutils

from datetime import datetime

"""
Get current time in UTC format.
"""
def get_current_time_utc():
    currenttime = datetime.utcnow()
    formattedtime, micro = currenttime.strftime('%Y-%m-%dT%H:%M:%S.%f').split('.')
    formattedtime = "%s.%03dZ" % (formattedtime, int(micro) / 1000)

    return formattedtime

def check_if_uuid(in_uuid):
    is_uuid = False
    try:
        uuid.UUID(in_uuid)
        is_uuid = True
    except Exception:
        is_uuid = False

    return is_uuid

def get_data_list(name, login_id, is_login, coll_contribution):
    resp = None
    is_error = False
    is_unauthorized = False

    if name != None:
        is_objectid = mongoutils.check_if_objectid(name)

        # query using either non-pii ObjectId or name
        if (is_objectid):
            id = ObjectId(name)
            if (is_login):
                db_data = mongoutils.query_dataset_by_objectid(coll_contribution, id, login_id, is_login)
                data_list = list(db_data)
            else:
                db_data = mongoutils.query_dataset_by_objectid_no_status(coll_contribution, id)
                data_list = list(db_data)
                if len(data_list) > 0:
                    if "status" not in data_list[0]:
                        msg = {
                            "reason": "Status is not in the dataset " + str(name),
                            "error": "Not Authorized: " + request.url,
                        }
                        msg_json = jsonutils.create_log_json("Contribution", "GET", msg)
                        logging.error("Contribution GET " + json.dumps(msg_json))
                        resp = rs_handlers.not_authorized(msg_json)
                        return data_list, is_objectid, True, resp
                    status = data_list[0]["status"]
                    if status != "Published":
                        msg = {
                            "reason": "Not authorized to view the contribution dataset with given id:" + str(name),
                            "error": "Not Authorized: " + request.url,
                        }
                        msg_json = jsonutils.create_log_json("Contribution", "GET", msg)
                        logging.error("Contribution GET " + json.dumps(msg_json))
                        resp = rs_handlers.not_authorized(msg_json)
                        return data_list, is_objectid, True, resp
            if len(data_list) > 1:
                msg = {
                    "reason": "There are more than 1 contribution record: " + str(name),
                    "error": "Bad Request: " + request.url,
                }
                msg_json = jsonutils.create_log_json("Contribution", "GET", msg)
                logging.error("Contribution GET " + json.dumps(msg_json))
                is_error = True
                resp = rs_handlers.bad_request(msg_json)
        else:
            if (is_login):
                db_data = mongoutils.query_dataset(coll_contribution, cfg.FIELD_NAME, name, login_id, is_login)
                data_list = list(db_data)
            else:
                db_data = mongoutils.query_dataset_no_status(coll_contribution,  cfg.FIELD_NAME, name)
                tmp_data_list = list(db_data)
                data_list = []
                for data in tmp_data_list:
                    if "status" in data:
                        status = data["status"]
                        if status == "Published":
                            data_list.append(data)
                        else:
                            is_unauthorized = True
        if len(data_list) == 0:
            if is_unauthorized:
                msg = {
                    "reason": "Not authorized to view the contribution dataset with given id:" + str(name),
                    "error": "Not Authorized: " + request.url,
                }
                msg_json = jsonutils.create_log_json("Contribution", "GET", msg)
                logging.error("Contribution GET " + json.dumps(msg_json))
                is_error = True
                resp = rs_handlers.not_authorized(msg_json)
            else:
                msg = {
                    "reason": "There is no contribution record: " + str(name),
                    "error": "Not Found: " + request.url,
                }
                msg_json = jsonutils.create_log_json("Contribution", "GET", msg)
                logging.error("Contribution GET " + json.dumps(msg_json))
                is_error = True
                resp = rs_handlers.not_found(msg_json)

        return data_list, is_objectid, is_error, resp

    else:
        msg = {
            "reason": "The contribution does not exist: " + str(name),
            "error": "Not Found: " + request.url,
        }
        msg_json = jsonutils.create_log_json("Contribution", "GET", msg)
        logging.error("Contribution GET " + json.dumps(msg_json))
        resp = rs_handlers.not_found(msg_json)

    return None, None, True, resp