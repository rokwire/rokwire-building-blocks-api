import json
import datetime
import logging
import uuid as uuidlib
import copy

from flask import jsonify, request, g
from bson import ObjectId

import controllers.configs as cfg
import utils.mongoutils as mongoutils
import utils.jsonutils as jsonutils
import utils.datasetutils as datasetutils
import utils.rest_handlers as rs_handlers
import utils.otherutils as otherutils
import utils.tokenutils as tokenutils
import utils.mongoutils as mongoutils

from utils import query_params
from models.pii_data import PiiData
from models.non_pii_data import NonPiiData


def post():
    is_new_install = True

    # check if uuid is in there otherwise it is either a first installation
    try:
        in_json = request.get_json()
        non_pii_uuid = in_json["uuid"]
        # even if there is non_pii_uuid is in the input json, it could be a new one
        # check if the dataset is existing with given uuid
        dataset = mongoutils.get_non_pii_dataset_from_field(cfg.FIELD_PROFILE_UUID, non_pii_uuid)
        if dataset is not None:
            is_new_install = False
            msg = {
                "reason": "UUID in input json already exists in the database: " + str(non_pii_uuid),
                "error": "Bad Request: " + request.url,
            }
            msg_json = jsonutils.create_log_json("Profile", "POST", msg)
            logging.error("POST " + json.dumps(json.loads(msg_json)))
            return rs_handlers.bad_request(msg)
    except:
        pass

    if is_new_install:
        # new installation of the app
        currenttime = datetime.datetime.now()
        currenttime = currenttime.strftime("%Y/%m/%dT%H:%M:%S")
        non_pii_dataset = NonPiiData('')
        non_pii_uuid = str(uuidlib.uuid4())
        non_pii_dataset.set_uuid(non_pii_uuid)
        non_pii_dataset.set_creation_date(currenttime)
        non_pii_dataset.set_last_modified_date(currenttime)
        dataset, id = mongoutils.insert_non_pii_dataset_to_mongodb(non_pii_dataset)
        profile_uuid = dataset["uuid"]

        # use this if it needs to return actual dataset
        dataset = jsonutils.remove_objectid_from_dataset(dataset)
        # out_json = mongoutils.construct_json_from_query_list(dataset)
        msg = "new profile with new uuid has been created: " + str(profile_uuid)
        msg_json = jsonutils.create_log_json("Profile", "POST", dataset)
        logging.info("POST " + json.dumps(msg_json))

        return rs_handlers.return_id(msg, 'uuid', profile_uuid)


def get(uuid=None):
    data_list, is_objectid, is_error, resp = get_data_list(uuid)
    if is_error:
        return resp
    out_json = jsonutils.remove_null_subcategory(data_list[0])
    msg_json = jsonutils.create_log_json("Profile", "GET", copy.copy(out_json))
    logging.info("GET " + json.dumps(msg_json))

    out_json = mongoutils.construct_json_from_query_list(out_json)

    return out_json


def put(uuid=None):
    try:
        in_json = request.get_json()
    except Exception as ex:
        msg = {
            "reason": "Json format error: " + str(uuid),
            "error": "Bad Request: " + request.url,
        }
        msg_json = jsonutils.create_log_json("Profile", "PUT", msg)
        logging.error("PUT " + json.dumps(msg_json))
        return rs_handlers.bad_request(msg_json)

    # check if the uuid is really existing in the database
    non_pii_dataset = mongoutils.get_non_pii_dataset_from_field(cfg.FIELD_PROFILE_UUID, uuid)

    if non_pii_dataset is None:
        msg = {
            "reason": "There is no profile dataset with given uuid: " + str(uuid),
            "error": "Not Found: " + request.url,
        }
        msg_json = jsonutils.create_log_json("Profile", "PUT", msg)
        logging.error("PUT " + json.dumps(msg_json))
        return rs_handlers.not_found(msg_json)

    # the level check in in_json should be performed
    level_ok, level = otherutils.check_privacy_level(in_json)
    if level_ok == False:
        msg = {
            "reason": "The given privacy level is not correct: " + str(level),
            "error": "Bad Request: " + request.url,
        }
        msg_json = jsonutils.create_log_json("Profile", "PUT", msg)
        logging.error("PUT " + json.dumps(msg_json))
        return rs_handlers.bad_request(msg_json)

    non_pii_dataset, restjson = datasetutils.update_non_pii_dataset_from_json(non_pii_dataset, in_json)
    currenttime = datetime.datetime.now()
    currenttime = currenttime.strftime("%Y/%m/%dT%H:%M:%S")
    non_pii_dataset.set_last_modified_date(currenttime)

    result, non_pii_dataset = mongoutils.update_non_pii_dataset_in_mongo_by_field(
        cfg.FIELD_PROFILE_UUID, uuid,
        non_pii_dataset)

    # update the json information that doesn't belong to data schema
    if len(restjson) > 0:
        result, non_pii_dataset = mongoutils.update_json_with_no_schema(cfg.FIELD_PROFILE_UUID, uuid,
                                                                        non_pii_dataset, restjson)

    if result is None:
        msg = {
            "reason": "Failed to update Profile dataset: " + str(uuid),
            "error": "Not Implemented: " + request.url,
        }
        msg_json = jsonutils.create_log_json("Profile", "PUT", msg)
        logging.error("PUT " + json.dumps(msg_json))
        return rs_handlers.not_implemented(msg_json)

    non_pii_dataset = jsonutils.remove_file_descriptor_from_dataset(non_pii_dataset)
    out_json = jsonutils.remove_null_subcategory(non_pii_dataset)
    msg_json = jsonutils.create_log_json("Profile", "PUT", copy.copy(out_json))
    logging.info("PUT " + json.dumps(msg_json))
    out_json = mongoutils.construct_json_from_query_list(out_json)

    return out_json


def delete(uuid=None):
    data_list, is_objectid, is_error, resp = get_data_list(uuid)
    if is_error:
        return resp

    if (is_objectid):
        mongoutils.db_profile.non_pii_collection.delete_one({cfg.FIELD_OBJECTID: id})
        msg = {"uuid": str(id)}
        msg_json = jsonutils.create_log_json("Profile", "DELETE", msg)
        logging.info("DELETE " + json.dumps(msg_json))
        return rs_handlers.entry_deleted('uuid', id)

    try:
        mongoutils.db_profile.non_pii_collection.delete_one({cfg.FIELD_PROFILE_UUID: uuid})
        msg = {"uuid": str(id)}
        msg_json = jsonutils.create_log_json("Profile", "DELETE", msg)
        logging.info("DELETE " + json.dumps(msg_json))
        return rs_handlers.entry_deleted('uuid', uuid)
    except:
        msg = {
            "reason": "Failed to delete. The dataset does not exist: " + str(uuid),
            "error": "Not Found: " + request.url,
        }
        msg_json = jsonutils.create_log_json("Profile", "DELETE", msg)
        logging.error("DELETE " + json.dumps(msg_json))
        return rs_handlers.not_found(msg_json)


def get_data_list(uuid):
    resp = None
    is_error = False

    if uuid != None:
        is_objectid = mongoutils.check_if_objectid(uuid)

        # query using either non-pii ObjectId or uuid
        if (is_objectid):
            id = ObjectId(uuid)
            db_data = mongoutils.query_non_pii_dataset_by_objectid(id)
        else:
            db_data = mongoutils.query_non_pii_dataset(cfg.FIELD_PROFILE_UUID, uuid)

        data_list = list(db_data)

        if len(data_list) > 1:
            msg = {
                "reason": "There are more than 1 profile record: " + str(uuid),
                "error": "Bad Request: " + request.url,
            }
            msg_json = jsonutils.create_log_json("Profile", "GET", msg)
            logging.error("GET " + json.dumps(msg_json))
            is_error = True
            resp = rs_handlers.bad_request(msg_json)
        elif len(data_list) == 0:
            msg = {
                "reason": "There is no profile record for the uuid: " + str(uuid),
                "error": "Not Found: " + request.url,
            }
            msg_json = jsonutils.create_log_json("Profile", "GET", msg)
            logging.error("GET " + json.dumps(msg_json))
            is_error = True
            resp = rs_handlers.not_found(msg_json)

        return data_list, is_objectid, is_error, resp

    else:
        msg = {
            "reason": "The profile does not exist: " + str(uuid),
            "error": "Not Found: " + request.url,
        }
        msg_json = jsonutils.create_log_json("Profile", "GET", msg)
        logging.error("GET " + json.dumps(msg_json))
        resp = rs_handlers.not_found(msg_json)

    return None, None, True, resp


def pii_post():
    # msg = {'message': 'POST info for PII:'}
    # resp = jsonify(msg)
    # resp.status_code = 200
    # logging.debug("POST " + json.dumps(msg))
    #
    # return resp

    # Get ID Token data from global context variable.
    auth_resp = g.user_token_data
    tk_uin, tk_firstname, tk_lastname, tk_email, tk_phone, tk_is_uin, tk_is_phone = tokenutils.get_data_from_token(
        auth_resp)

    is_new_entry = False
    # Todo following variable should be revived if the email or phone number can get updated
    # auth_pass = False

    try:
        in_json = request.get_json()
    except Exception as ex:
        msg = {
            "reason": "Json format error.",
            "error": "Bad Request: " + request.url,
        }
        msg_json = jsonutils.create_log_json("PII", "POST", msg)
        logging.error("PII POST " + json.dumps(msg_json))
        return rs_handlers.bad_request(msg_json)

    # get uuid, if failed it is a bad request
    try:
        non_pii_uuid = in_json[cfg.FIELD_PROFILE_UUID]
        if isinstance(non_pii_uuid, list) == False:
            # # this is an error routine when it is not a list
            # # for now, this should be commented out because the endpoint will accept both string and list
            # # after chaning the app only send uuid as a list, following lines should be revived
            # msg = {
            #     "reason": "The uuid information is not a list.",
            #     "error": "Json format error."
            # }
            # msg_json = jsonutils.create_log_json("PII", "POST", msg)
            # logging.error("PII POST " + json.dumps(msg_json))
            # return rs_handlers.bad_request(msg_json)

            # if non_pii_uuid is not a list,
            # we assume that it is a single string uuid object so convert this to a list with single item
            tmp_list = []
            tmp_list.append(non_pii_uuid)
            non_pii_uuid = tmp_list
    except Exception as ex:
        msg = {
            "reason": "uuid not supplied.",
            "error": "Bad Request: " + request.url,
        }
        msg_json = jsonutils.create_log_json("PII", "POST", msg)
        logging.error("PII POST " + json.dumps(msg_json))
        return rs_handlers.bad_request(msg_json)

    # get non_pii_uuid value from the list
    if len(non_pii_uuid) > 0:
        non_pii_uuid = non_pii_uuid[0]
    else:
        msg = {
            "reason": "uuid list is empty.",
            "error": "Bad Request: " + request.url,
        }
        msg_json = jsonutils.create_log_json("PII", "POST", msg)
        logging.error("PII POST " + json.dumps(msg_json))
        return rs_handlers.bad_request(msg_json)

    # check if it is a new record or existing record
    try:
        pid = in_json[cfg.FIELD_PID]
        dataset = mongoutils.get_pii_dataset_from_field(cfg.FIELD_PROFILE_UUID, pid)

        # if it is an existing entry, then check if the information in db matches with the id token
        auth_pass = check_auth(dataset, tk_uin, tk_phone, tk_is_uin, tk_is_phone)
    except:
        dataset = None
        is_new_entry = True

    # check if the email already exists
    if tk_is_uin:
        try:
            dataset = mongoutils.get_pii_dataset_from_field('uin', tk_uin)
            # if there is a dataset, it means that the email is existing in the database
            if dataset is not None:
                # ToDo Following lines will be commented out due to the following assumption
                # that the email in the database doesn't get updated so, no change in email.
                # However, if there is email update available, the following part should be revived.
                # # check if the id token and db info matches
                # if not (auth_pass):
                #     msg = {
                #         "reason": "The user info in id token and db are not matching.",
                #         "error": "Authorization Failed."
                #     }
                #     msg_json = jsonutils.create_log_json("PII", "POST", msg)
                #     self.logger.error("PII POST " + json.dumps(msg_json))
                #     return jsonutils.create_auth_fail_message()
                #
                # if not (auth_pass):
                #     msg = {
                #         "reason": "The user info in id token and db are not matching.",
                #         "error": "Authorization Failed."
                #     }
                #     msg_json = jsonutils.create_log_json("PII", "POST", msg)
                #     self.logger.error("PII POST " + json.dumps(msg_json))
                #     return jsonutils.create_auth_fail_message()

                pid = dataset.get_pid()
                non_pii_uuid_from_dataset = dataset.uuid
                dataset = append_non_pii_uuid(non_pii_uuid, non_pii_uuid_from_dataset, dataset)
                currenttime = otherutils.get_current_time_utc()
                dataset.set_last_modified_date(currenttime)
                result, pii_dataset = mongoutils.update_pii_dataset_in_mongo_by_field(cfg.FIELD_PID, pid, dataset)
                msg = {
                    "reason": "UIN already exists: " + str(pid),
                    "warning": "UIN already exists: " + request.url,
                }
                msg_json = jsonutils.create_log_json("PII", "POST", msg)
                logging.warning("PII POST " + json.dumps(msg_json))
                return rs_handlers.return_id('UIN already exists.', 'pid', pid)
        except:
            return rs_handlers.internal_server_error()

    # check if the phonenumber already exists
    if tk_is_phone:
        try:
            dataset = mongoutils.get_pii_dataset_from_field('phone', tk_phone)

            # ToDo Following lines will be commented out due to the following assumption
            # that the email in the database doesn't get updated so, no change in email.
            # However, if there is email update available, the following part should be revived.
            # check if the id token and db info matches
            # if not (auth_pass):
            #     auth_pass = self.check_auth(dataset, tk_uin, tk_phone, tk_is_uin, tk_is_phone)
            #
            # if not (auth_pass):
            #     msg = {
            #         "reason": "The user info in id token and db are not matching.",
            #         "error": "Authorization Failed."
            #     }
            #     msg_json = jsonutils.create_log_json("PII", "POST", msg)
            #     self.logger.error("PII POST " + json.dumps(msg_json))
            #     return jsonutils.create_auth_fail_message()

            if dataset is not None:
                pid = dataset.get_pid()
                non_pii_uuid_from_dataset = dataset.uuid
                dataset = append_non_pii_uuid(non_pii_uuid, non_pii_uuid_from_dataset, dataset)
                currenttime = otherutils.get_current_time_utc()
                dataset.set_last_modified_date(currenttime)
                result, pii_dataset = mongoutils.update_pii_dataset_in_mongo_by_field(cfg.FIELD_PID, pid, dataset)
                msg = {
                    "reason": "Phone number already exists: " + str(pid),
                    "warning": "Phone number already exists: " + request.url,
                }
                msg_json = jsonutils.create_log_json("PII", "POST", msg)
                logging.warning("PII POST " + json.dumps(msg_json))
                return rs_handlers.return_id('Phone number already exists.', 'pid', pid)
        except:
            return rs_handlers.internal_server_error()

    if dataset is not None:
        is_new_entry = False

    pii_dataset = PiiData(in_json)

    if is_new_entry:
        # insert new pii_dataset
        currenttime = otherutils.get_current_time_utc()
        pid = str(uuidlib.uuid4())
        pii_dataset.set_pid(pid)
        non_pii_uuid_from_dataset = []
        non_pii_uuid_from_dataset.append(non_pii_uuid)
        pii_dataset.set_uuid(non_pii_uuid_from_dataset)
        pii_dataset.set_creation_date(currenttime)
        pii_dataset.set_last_modified_date(currenttime)

        # update dataset from id token info
        if tk_firstname is not None:
            pii_dataset.set_firstname(tk_firstname)
        if tk_lastname is not None:
            pii_dataset.set_lastname(tk_lastname)
        if tk_email is not None:
            pii_dataset.set_email(tk_email)
        if tk_phone is not None:
            pii_dataset.set_phone(tk_phone)
        if tk_uin is not None:
            pii_dataset.set_uin(tk_uin)
        pii_dataset = mongoutils.insert_pii_dataset_to_mongodb(pii_dataset)

        if pii_dataset is None:
            msg = {
                "reason": "Failed to update profile uuid into pii dataset: " + str(pid),
                "error": "Not Implemented: " + request.url,
            }
            msg_json = jsonutils.create_log_json("PII", "POST", msg)
            logging.error("PII POST " + json.dumps(msg_json))
            return rs_handlers.not_implemented(msg_json)

        msg = "Pii data has been posted with : " + str(pid)
        msg_json = jsonutils.create_log_json("PII", "POST", jsonutils.remove_objectid_from_dataset(pii_dataset))
        logging.info("PII POST " + json.dumps(msg_json))
        return rs_handlers.return_id(msg, 'pid', pid)
    else:
        msg = {
            "reason": "The request is wrong or the entry already exists: " + str(pid),
            "error": "Bad Request: " + request.url,
        }
        msg_json = jsonutils.create_log_json("PII", "POST", msg)
        logging.error("PII POST " + json.dumps(msg_json))
        return rs_handlers.bad_request(msg_json)

def device_data_search():
    args = request.args
    query = dict()
    try:
        query = query_params.format_query_device_data(args, query)
    except Exception as ex:
        msg = {
            "reason": "The query is wrong or bad argument " + str(args),
            "error": "Bad Request: " + request.url,
        }
        msg_json = jsonutils.create_log_json("Device Data", "SEARCH", msg)
        logging.error("Device Data SEARCH " + json.dumps(msg_json))
        return rs_handlers.bad_request(msg_json)

    try:
        out_json = mongoutils.get_profile_result(query)
    except Exception as ex:
        msg = {
            "reason": "There is no result " + str(args),
            "error": "No Result: " + request.url,
        }
        msg_json = jsonutils.create_log_json("Device Data", "SEARCH", msg)
        logging.error("Device Data SEARCH " + json.dumps(msg_json))
        return rs_handlers.not_found(msg_json)

    if out_json is not None:
        # TODO if the out_json only need to contain device token and uuid, perform following.
        #  Otherwise just leave out_json as it is
        out_json = build_favorites_eventid_result(out_json)

        msg = {
            "search": "Device Data search performed with arguments of : " + str(args),
            "result": out_json,
        }
        msg_json = jsonutils.create_log_json("Device Data", "SEARCH", msg)
        logging.info("Device Data SEARCH " + json.dumps(msg))

        return out_json
    else:
        msg = {
            "reason": "There is no result " + str(args),
            "error": "No Result: " + request.url,
        }
        msg_json = jsonutils.create_log_json("Device Data", "SEARCH", msg)
        logging.error("Device Data SEARCH " + json.dumps(msg_json))
        return rs_handlers.not_found(msg_json)

def build_favorites_eventid_result(in_json):
    if isinstance(in_json, list):  # json list
        out_list = []
        for single_json in in_json:
            tmp_json = {}
            tmp_json["uuid"] = single_json["uuid"]
            try:
                tmp_json['fcmTokens'] = single_json["fcmTokens"]
            except:
                pass
            out_list.append(tmp_json)
        out_json = out_list
    else:
        out_json = {}
        out_json["uuid"] = in_json["uuid"]
        try:
            out_json['fcmTokens'] = in_json["fcmTokens"]
        except:
            pass
    return out_json

def append_non_pii_uuid(non_pii_uuid, non_pii_uuid_from_dataset, pii_dataset):
    is_non_pii_uuid_in_json_new = True
    # check if non-pii-uuid is already in there
    for i in range(len(non_pii_uuid_from_dataset)):
        if non_pii_uuid == non_pii_uuid_from_dataset[i]:
            is_non_pii_uuid_in_json_new = False

    # adde non-pii uuid in json only if it is new uuid
    if is_non_pii_uuid_in_json_new:
        non_pii_uuid_from_dataset.append(non_pii_uuid)

    return pii_dataset


def check_auth(self, dataset, tk_uin, tk_phone, tk_is_uin, tk_is_phone):
    auth_pass = False
    if dataset:
        if tk_is_uin:
            if dataset.get_uin() == tk_uin:
                auth_pass = True
        if tk_is_phone:
            if dataset.get_phone() == tk_phone:
                auth_pass = True

    return auth_pass

# def pii_put(pid=None):
#     msg = {'message': 'PUT info for PII:'}
#     resp = jsonify(msg)
#     resp.status_code = 200
#     logging.debug("PUT " + json.dumps(msg))
#
#     return resp
#
# def pii_delete(pid=None):
#     msg = {'message': 'DELETE info for PII:'}
#     resp = jsonify(msg)
#     resp.status_code = 200
#     logging.debug("DELETE " + json.dumps(msg))
#
#     return resp


def get_data_list_pid(pid):
    is_error = False
    resp = None

    if pid != None:
        is_objectid = mongoutils.check_if_objectid(pid)

        # query using either non-pii ObjectId or uuid
        if (is_objectid):
            id = ObjectId(pid)
            db_data = mongoutils.query_pii_dataset_by_objectid(id)
        else:
            db_data = mongoutils.query_pii_dataset(cfg.FIELD_PID, pid)

        data_list = list(db_data)
        if len(data_list) > 1:
            msg = {
                "reason": "There are more than 1 pii record: " + str(pid),
                "error": "Bad Request: " + request.url,
            }
            msg_json = jsonutils.create_log_json("PII", "GET", msg)
            logging.error("PII GET " + json.dumps(msg_json))
            is_error = True
            resp = rs_handlers.bad_request(msg_json)

            return None, None, is_error, resp

        if len(data_list) == 0:
            msg = {
                "reason": "There is no pii record for the pid: " + str(pid),
                "error": "Not Found: " + request.url,
            }
            msg_json = jsonutils.create_log_json("PII", "GET", msg)
            logging.error("PII GET " + json.dumps(msg_json))
            is_error = True
            resp = rs_handlers.not_found(msg_json)

            return None, None, is_error, resp

        if len(data_list) > 0:
            return data_list, is_objectid, is_error, resp

    else:
        msg = {
            "reason": "Pii dataset does not exist: " + str(pid),
            "error": "Not Found: " + request.url,
        }
        msg_json = jsonutils.create_log_json("PII", "GET", msg)
        logging.error("PII GET " + json.dumps(msg_json))
        is_error = True
        resp = rs_handlers.not_found(msg_json)

        return None, None, is_error, resp


def check_id(id_token, data_list):
    id_type, id_string = tokenutils.get_id_info_from_token(id_token)
    auth_pass = False

    if id_type == 1:  # Shibboleth ID Token
        # get id info from data_list
        id_from_db = data_list['uin']
        if id_from_db == id_string:
            auth_pass = True
    elif id_type == 2:  # Phone ID Token
        # get phone number from data_list
        id_from_db = data_list['phone']
        if id_from_db == id_string:
            auth_pass = True

    return auth_pass


def pii_get(pid=None):
    # Get ID Token data from global context variable.
    auth_resp = g.user_token_data

    data_list, is_objectid, is_error, resp = get_data_list_pid(pid)
    if is_error:
        return resp

    auth_pass = check_id(auth_resp, data_list[0])

    if not (auth_pass):
        msg = {
            "reason": "The user info in id token and db are not matching.",
            "error": "Authorization Failed."
        }
        msg_json = jsonutils.create_log_json("PII", "GET", msg)
        logging.error("PII GET " + json.dumps(msg_json))
        return jsonutils.create_auth_fail_message()

    # remove fileDescriptors from db_data
    data_list = jsonutils.remove_file_descriptor_from_data_list(data_list)
    out_json = mongoutils.construct_json_from_query_list(data_list[0])
    msg_json = jsonutils.create_log_json("PII", "GET", data_list[0])
    logging.info("PII GET " + json.dumps(jsonutils.remove_objectid_from_dataset(msg_json)))

    return out_json


def pii_put(pid=None):
    # Get ID Token data from global context variable.
    auth_resp = g.user_token_data
    tk_uin, tk_firstname, tk_lastname, tk_email, tk_phone, tk_is_uin, tk_is_phone = tokenutils.get_data_from_token(
        auth_resp)

    try:
        in_json = request.get_json()
        # ToDo following lines are commented out for now
        #  but it should be used if the email and phone number get updated
        # # if there is any phone number or email information in input json, they will be removed
        # # since the current policy is not updating the email or phone number
        # # until further decision
        # try:
        #     del in_json["uin"]
        # except:
        #     pass
        # try:
        #     del in_json["phone"]
        # except:
        #     pass

    except Exception as ex:
        msg = {
            "reason": "Json format error: " + str(pid),
            "error": "Bad Request: " + request.url,
        }
        msg_json = jsonutils.create_log_json("PII", "PUT", msg)
        logging.error("PII PUT " + json.dumps(msg_json))
        return rs_handlers.bad_request(msg_json)

    # check if the pid is really existing in the database
    pii_dataset = mongoutils.get_pii_dataset_from_field(cfg.FIELD_PID, pid)

    if pii_dataset == None:
        msg = {
            "reason": "There is no dataset with given pii uuid: " + str(pid),
            "error": "Not Found: " + request.url,
        }
        msg_json = jsonutils.create_log_json("PII", "PUT", msg)
        logging.error("PII PUT " + json.dumps(msg_json))
        return rs_handlers.not_found(msg_json)

    tmp_dataset = json.loads(json.dumps(pii_dataset.__dict__))
    auth_pass = check_id(auth_resp, tmp_dataset)

    if not (auth_pass):
        msg = {
            "reason": "The user info in id token and db are not matching.",
            "error": "Authorization Failed."
        }
        msg_json = jsonutils.create_log_json("PII", "PUT", msg)
        logging.error("PII PUT " + json.dumps(msg_json))
        return jsonutils.create_auth_fail_message()

    pii_dataset = datasetutils.update_pii_dataset_from_json(pii_dataset, in_json)
    currenttime = otherutils.get_current_time_utc()

    pii_dataset.set_last_modified_date(currenttime)

    # update pii_dataset's non_pii_uuid
    non_pii_uuid_from_dataset = pii_dataset.get_uuid()
    try:
        non_pii_uuid = in_json[cfg.FIELD_PROFILE_UUID]
        # both non_pii_uuid and non_pii_uuid_from_dataset should be list
        if (type(non_pii_uuid) is not list) or (type(non_pii_uuid_from_dataset) is not list):
            msg = {
                "reason": "The uuid information is not a list.",
                "error": "Json format error."
            }
            msg_json = jsonutils.create_log_json("PII", "PUT", msg)
            logging.error("PII PUT " + json.dumps(msg_json))
            return rs_handlers.bad_request(msg_json)

        pii_dataset.set_uuid(non_pii_uuid)
        # # the following lines can be used for item to item comparison and append when it is needed
        # for i in range(len(non_pii_uuid)):
        #     pii_dataset = append_non_pii_uuid(non_pii_uuid[i], non_pii_uuid_from_dataset, pii_dataset)
    except:
        pass

    # update dataset from id token info
    if tk_firstname is not None:
        pii_dataset.set_firstname(tk_firstname)
    if tk_lastname is not None:
        pii_dataset.set_lastname(tk_lastname)
    if tk_email is not None:
        pii_dataset.set_email(tk_email)
    if tk_phone is not None:
        pii_dataset.set_phone(tk_phone)
    if tk_uin is not None:
        pii_dataset.set_uin(tk_uin)

    result, pii_dataset = mongoutils.update_pii_dataset_in_mongo_by_field(cfg.FIELD_PID, pid,
                                                                          pii_dataset)

    if result is None:
        msg = {
            "reason": "Failed to update non pii uuid into pii dataset: " + str(pid),
            "error": "Not Implemented: " + request.url,
        }
        msg_json = jsonutils.create_log_json("PII", "PUT", msg)
        logging.error("PII PUT " + json.dumps(msg_json))
        return rs_handlers.not_implemented(msg_json)

    pii_dataset = jsonutils.remove_file_descriptor_from_dataset(pii_dataset)
    out_json = mongoutils.construct_json_from_query_list(pii_dataset)
    msg_json = jsonutils.create_log_json("PII", "PUT", jsonutils.remove_objectid_from_dataset(pii_dataset))
    logging.info("PII PUT " + json.dumps(jsonutils.remove_objectid_from_dataset(msg_json)))
    return out_json


def pii_delete(pid=None):
    # Get ID Token data from global context variable.
    auth_resp = g.user_token_data

    data_list, is_objectid, is_error, resp = get_data_list_pid(pid)
    if is_error:
        return resp

    auth_pass = check_id(auth_resp, data_list[0])

    if not (auth_pass):
        msg = {
            "reason": "The user info in id token and db are not matching.",
            "error": "Authorization Failed."
        }
        msg_json = jsonutils.create_log_json("PII", "DELETE", msg)
        logging.error("PII DELETE " + json.dumps(msg_json))
        return jsonutils.create_auth_fail_message()

    if (is_objectid):
        mongoutils.db_pii.pii_collection.delete_one({cfg.FIELD_OBJECTID: id})
        msg = {"pid": str(pid)}
        msg_json = jsonutils.create_log_json("PII", "DELETE", msg)
        logging.info("PII DELETE " + json.dumps(msg_json))
        return rs_handlers.entry_deleted('pid', id)

    try:
        mongoutils.db_pii.pii_collection.delete_one({cfg.FIELD_PID: pid})
        msg = {"pid": str(pid)}
        msg_json = jsonutils.create_log_json("PII", "DELETE", msg)
        logging.info("PII DELETE " + json.dumps(msg_json))
        return rs_handlers.entry_deleted('pid', pid)
    except:
        msg = {
            "reason": "Failed to deleted pii. not found: " + str(pid),
            "error": "Not Found: " + request.url,
        }
        msg_json = jsonutils.create_log_json("PII", "DELETE", msg)
        logging.info("PII DELETE " + json.dumps(msg_json))
        return rs_handlers.not_found(msg_json)