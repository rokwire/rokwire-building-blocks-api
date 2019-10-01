import sys
import json

sys.path.append('../../')
import datetime
import logging
import uuid as uuidlib
import copy

from flask import Flask, request
from flask_restful import Resource, Api
from bson import ObjectId
from time import gmtime

import auth_middleware
import profileservice.configs as cfg
import profileservice.restservice.utils.mongoutils as mongoutils
import profileservice.restservice.utils.jsonutils as jsonutils
import profileservice.restservice.utils.datasetutils as datasetutils
import profileservice.restservice.utils.rest_handlers as rs_handlers
import profileservice.restservice.utils.otherutils as otherutils
import profileservice.restservice.utils.tokenutils as tokenutils

from profileservice.dao.pii_data import PiiData
from profileservice.dao.non_pii_data import NonPiiData
from profileservice.restservice.utils.otherutils import create_file_descriptor

app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False

mongoutils.index_non_pii_data()
mongoutils.index_pii_data()


"""
profile rest service root directory
"""


# Note that this corresponds to the ../profiles/{uuid} end points, as opposed to the profiles/pii endpoints.
class NonPiiRootDir(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')

    def post(self):
        auth_middleware.verify_secret(request)

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
                msg = "{\"reason\": \"UUID in input json already exists in the database: " + str(non_pii_uuid) + "\"}"
                msg_json = jsonutils.create_log_json("Profile", "POST", json.loads(msg))
                msg_json['error'] = 'Bad Request: ' + request.url
                self.logger.error("POST " + json.dumps(json.loads(msg_json)))
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
            self.logger.info("POST " + json.dumps(msg_json))

            return rs_handlers.return_id(msg, 'uuid', profile_uuid)

"""
provide profile information by profile id or remove it
"""


class DealNonPii(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')

    def get_data_list(self, uuid):
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
                msg = "{\"reason\": \"There are more than 1 profile record: " + str(uuid) + "\"}"
                msg_json = jsonutils.create_log_json("Profile", "GET", json.loads(msg))
                msg_json['error'] = 'Bad Request: ' + request.url
                self.logger.error("GET " + json.dumps(msg_json))
                is_error = True
                resp = rs_handlers.bad_request(msg_json)
            elif len(data_list) == 0:
                msg = "{\"reason\": \"There is no profile record for the uuid: " + str(uuid) + "\"}"
                msg_json = jsonutils.create_log_json("Profile", "GET", json.loads(msg))
                msg_json['error'] = 'Bad Request: ' + request.url
                self.logger.error("GET " + json.dumps(msg_json))
                is_error = True
                resp = rs_handlers.bad_request(msg_json)

            return data_list, is_objectid, is_error, resp

        else:
            msg = "{\"reason\": \"The profile does not exist: " + str(uuid) + "\"}"
            msg_json = jsonutils.create_log_json("Profile", "GET", json.loads(msg))
            msg_json['error'] = 'Not Found: ' + request.url
            self.logger.error("GET " + json.dumps(msg_json))
            resp = rs_handlers.not_found(msg_json)

            return None, None, True, resp

    def get(self, uuid):
        auth_middleware.verify_secret(request)

        data_list, is_objectid, is_error, resp = self.get_data_list(uuid)
        if is_error:
            return resp
        out_json = jsonutils.remove_null_subcategory(data_list[0])
        msg_json = jsonutils.create_log_json("Profile", "GET", copy.copy(out_json))
        self.logger.info("GET " + json.dumps(msg_json))

        out_json = mongoutils.construct_json_from_query_list(out_json)

        return out_json

    def put(self, uuid):
        auth_middleware.verify_secret(request)

        try:
            in_json = request.get_json()
        except Exception as ex:
            msg = "{\"reason\": \"json format error: " + str(uuid) + "\"}"
            msg_json = jsonutils.create_log_json("Profile", "PUT", json.loads(msg))
            msg_json['error'] = 'Bad Request: ' + request.url
            self.logger.error("PUT " + json.dumps(msg_json))
            return rs_handlers.bad_request(msg_json)

        # check if the uuid is really existing in the database
        non_pii_dataset = mongoutils.get_non_pii_dataset_from_field(cfg.FIELD_PROFILE_UUID, uuid)

        if non_pii_dataset is None:
            msg = "{\"reason\": \"There is no profile dataset with given uuid: " + str(uuid) + "\"}"
            msg_json = jsonutils.create_log_json("Profile", "PUT", json.loads(msg))
            msg_json['error'] = 'Not Found: ' + request.url
            self.logger.error("PUT " + json.dumps(msg_json))
            return rs_handlers.not_found(msg_json)

        # the level check in in_json should be performed
        level_ok, level = otherutils.check_privacy_level(in_json)
        if level_ok == False:
            msg = "{\"reason\": \"The given privacy level is not correct: " + str(level) + "\"}"
            msg_json = jsonutils.create_log_json("Profile", "PUT", json.loads(msg))
            msg_json['error'] = 'Bad Request: ' + request.url
            self.logger.error("PUT " + json.dumps(msg_json))
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
            msg = "{\"reason\": \"Failed to update non Profile dataset: " + str(uuid) + "\"}"
            msg_json = jsonutils.create_log_json("Profile", "PUT", json.loads(msg))
            msg_json['error'] = 'Not Implemented: ' + request.url
            self.logger.error("PUT " + json.dumps(msg_json))
            return rs_handlers.not_implemented(msg_json)

        non_pii_dataset = jsonutils.remove_file_descriptor_from_dataset(non_pii_dataset)
        out_json = jsonutils.remove_null_subcategory(non_pii_dataset)
        msg_json = jsonutils.create_log_json("Profile", "PUT", copy.copy(out_json))
        self.logger.info("PUT " + json.dumps(msg_json))
        out_json = mongoutils.construct_json_from_query_list(out_json)

        return out_json

    def delete(self, uuid):
        auth_middleware.verify_secret(request)

        data_list, is_objectid, is_error, resp = self.get_data_list(uuid)
        if is_error:
            return resp

        if (is_objectid):
            mongoutils.db_profile.non_pii_collection.delete_one({cfg.FIELD_OBJECTID: id})
            msg = "{\"uuid\": \"" + str(id) + "\"}"
            msg_json = jsonutils.create_log_json("Profile", "DELETE", json.loads(msg))
            self.logger.info("DELETE " + json.dumps(msg_json))
            return rs_handlers.entry_deleted('uuid', id)

        try:
            mongoutils.db_profile.non_pii_collection.delete_one({cfg.FIELD_PROFILE_UUID: uuid})
            msg = "{\"uuid\": \"" + str(uuid) + "\"}"
            msg_json = jsonutils.create_log_json("Profile", "DELETE", json.loads(msg))
            self.logger.info("DELETE " + json.dumps(msg_json))
            return rs_handlers.entry_deleted('uuid', uuid)
        except:
            msg = "{\"reason\": \"failed to deleted. the dataset does not exist: " + str(uuid) + "\"}"
            msg_json = jsonutils.create_log_json("Profile", "DELETE", json.loads(msg))
            msg_json['error'] = 'Not Found: ' + request.url
            self.logger.error("DELETE " + json.dumps(msg_json))
            return rs_handlers.not_found(msg_json)


""""
get or post pii dataset
"""


# These correspond to call to the /profiles/pii endpoint
class PiiRootDir(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')

    def get(self):
        auth_middleware.authenticate()

        term_pid = request.args.get('pid', None)
        term_username = request.args.get('username', None)
        term_phone = request.args.get('phone', None)
        term_email = request.args.get('email', None)

        # TODO this if else method should smarter like case or something else
        if term_pid != None:
            out_json = mongoutils.get_pii_http_output_query_result_using_field_string(cfg.FIELD_PID, term_pid)
            if out_json == None:
                return rs_handlers.not_found()
            return out_json
        if term_username != None:
            out_json = mongoutils.get_pii_http_output_query_result_using_field_string('username', term_username)
            if out_json == None:
                return rs_handlers.not_found()
            return out_json
        if term_phone != None:
            out_json = mongoutils.get_pii_http_output_query_result_using_field_string('phone', term_phone)
            if out_json == None:
                return rs_handlers.not_found()
            return out_json
        if term_email != None:
            out_json = mongoutils.get_pii_http_output_query_result_using_field_string('email', term_email)
            if out_json == None:
                return rs_handlers.not_found()
            return out_json

    def post(self):
        auth_middleware.authenticate()

        is_new_entry = False
        try:
            in_json = request.get_json()
        except Exception as ex:
            msg = "{\"reason\": \"json format error: \"}"
            msg_json = jsonutils.create_log_json("PII", "POST", json.loads(msg))
            msg_json['error'] = 'Bad Request: ' + request.url
            self.logger.error("PII POST " + json.dumps(msg_json))
            return rs_handlers.bad_request(msg_json)

        # get uuid, if failed it is a bad request
        try:
            non_pii_uuid = in_json[cfg.FIELD_PROFILE_UUID]
        except Exception as ex:
            msg = "{\"reason\": \"uuid not supplied\"}"
            msg_json = jsonutils.create_log_json("PII", "POST", json.loads(msg))
            msg_json['error'] = 'Bad Request: ' + request.url
            self.logger.error("PII POST " + json.dumps(msg_json))
            return rs_handlers.bad_request(msg_json)

        # check if it is a new record or existing record
        try:
            pid = in_json[cfg.FIELD_PID]
            dataset = mongoutils.get_pii_dataset_from_field(cfg.FIELD_PROFILE_UUID, pid)
        except:
            dataset = None
            is_new_entry = True

        # check if the email already exists
        try:
            email = in_json['email']
            dataset = mongoutils.get_pii_dataset_from_field('email', email)
            if dataset is not None:
                pid = dataset.get_pid()
                msg = "{\"reason\": \"Email already existst: " + str(pid) + "\"}"
                msg_json = jsonutils.create_log_json("PII", "POST", json.loads(msg))
                msg_json['warning'] = 'Email already exists: ' + request.url
                self.logger.warning("PII POST " + json.dumps(msg_json))
                return rs_handlers.return_id('Email already exists.', 'pid', pid)
        except:
            pass

        # check if the phonenumber already exists
        try:
            phone = in_json['phone']
            dataset = mongoutils.get_pii_dataset_from_field('phone', phone)
            if dataset is not None:
                pid = dataset.get_pid()
                msg = "{\"reason\": \"Phone number already existst: " + str(pid) + "\"}"
                msg_json = jsonutils.create_log_json("PII", "POST", json.loads(msg))
                msg_json['warning'] = 'Phone number already exists: ' + request.url
                self.logger.error("PII POST " + json.dumps(msg_json))
                return rs_handlers.return_id('Phone number already exists.', 'pid', pid)
        except:
            pass

        if dataset is not None:
            is_new_entry = False

        pii_dataset = PiiData(in_json)

        if is_new_entry:
            # insert new pii_dataset
            currenttime = datetime.datetime.now()
            currenttime = currenttime.strftime("%Y/%m/%dT%H:%M:%S")
            pid = str(uuidlib.uuid4())
            pii_dataset.set_pid(pid)
            non_pii_uuid_from_dataset = []
            non_pii_uuid_from_dataset.append(non_pii_uuid)
            pii_dataset.set_uuid(non_pii_uuid_from_dataset)
            pii_dataset.set_creation_date(currenttime)
            pii_dataset.set_last_modified_date(currenttime)
            pii_dataset = mongoutils.insert_pii_dataset_to_mongodb(pii_dataset)

            if pii_dataset is None:
                msg = "{\"reason\": \"Failed to update non pii uuid into pii dataset: " + str(pid) + "\"}"
                msg_json = jsonutils.create_log_json("PII", "POST", json.loads(msg))
                msg_json['error'] = 'Not Implemented: ' + request.url
                self.logger.error("PII POST " + json.dumps(msg_json))
                return rs_handlers.not_implemented(msg_json)

            msg = "Pii data has been posted with : " + str(pid)
            msg_json = jsonutils.create_log_json("PII", "POST", jsonutils.remove_objectid_from_dataset(pii_dataset))
            self.logger.info("PII POST " + json.dumps(msg_json))
            return rs_handlers.return_id(msg, 'pid', pid)
        else:
            msg = "{\"reason\": \"The request is wrong or the entry already exists: " + str(pid) + "\"}"
            msg_json = jsonutils.create_log_json("PII", "POST", json.loads(msg))
            msg_json['error'] = 'Bad Request: ' + request.url
            self.logger.error("PII POST " + json.dumps(msg_json))
            return rs_handlers.bad_request(msg_json)


"""
provide profile information by profile id or remove it
"""


class DealPii(Resource):
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logger')

    def get_data_list(self, pid):
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
                msg = "{\"reason\": \"There are more than 1 pii record: " + str(pid) + "\"}"
                msg_json = jsonutils.create_log_json("PII", "GET", json.loads(msg))
                msg_json['error'] = 'Bad Request: ' + request.url
                self.logger.error("PII GET " + json.dumps(msg_json))
                is_error = True
                resp = rs_handlers.bad_request(msg_json)

                return None, None, is_error, resp

            if len(data_list) == 0:
                msg = "{\"reason\": \"There is no pii record for the pid: " + str(pid) + "\"}"
                msg_json = jsonutils.create_log_json("PII", "GET", json.loads(msg))
                msg_json['error'] = 'Bad Request: ' + request.url
                self.logger.error("PII GET " + json.dumps(msg_json))
                is_error = True
                resp = rs_handlers.bad_request(msg_json)

                return None, None, is_error, resp

            if len(data_list) > 0:
                return data_list, is_objectid, is_error, resp

        else:
            msg = "{\"reason\": \"Pii dataset does not exist: " + str(pid) + "\"}"
            msg_json = jsonutils.create_log_json("PII", "GET", json.loads(msg))
            msg_json['error'] = 'Not Found: ' + request.url
            self.logger.error("PII GET " + json.dumps(msg_json))
            is_error = True
            resp = rs_handlers.not_found(msg_json)

            return None, None, is_error, resp

    def check_id(self, id_token, data_list):
        id_type, id_string = tokenutils.get_id_info_from_token(id_token)
        auth_pass = False

        if id_type == 1:  # pii data
            # get uin from data_list
            uin = data_list['uin']
            if str(uin) == str(id_string):
                auth_pass = True
        elif id_type == 2:  # non-pii data
            # get phone number from data_list
            phone_number = data_list['phone']
            if str(phone_number) == str(id_string):
                auth_pass = True

        return auth_pass

    def get(self, pid):
        auth_resp = auth_middleware.authenticate()

        data_list, is_objectid, is_error, resp = self.get_data_list(pid)
        if is_error:
            return resp

        auth_pass = self.check_id(auth_resp, data_list[0])

        if not (auth_pass):
            return jsonutils.create_auth_fail_message()

        # remove fileDescriptors from db_data
        data_list = jsonutils.remove_file_descriptor_from_data_list(data_list)
        out_json = mongoutils.construct_json_from_query_list(data_list[0])
        msg_json = jsonutils.create_log_json("PII", "GET", data_list[0])
        self.logger.info("PII GET " + json.dumps(jsonutils.remove_objectid_from_dataset(msg_json)))

        return out_json

    def put(self, pid):
        auth_resp = auth_middleware.authenticate()

        try:
            in_json = request.get_json()
        except Exception as ex:
            msg = "{\"reason\": \"json format error: " + str(pid) + "\"}"
            msg_json = jsonutils.create_log_json("PII", "PUT", json.loads(msg))
            msg_json['error'] = 'Bad Request: ' + request.url
            self.logger.error("PII PUT " + json.dumps(msg_json))
            return rs_handlers.bad_request(msg_json)

        # check if the pid is really existing in the database
        pii_dataset = mongoutils.get_pii_dataset_from_field(cfg.FIELD_PID, pid)

        if pii_dataset == None:
            msg = "{\"reason\": \"There is no dataset with given pii uuid: " + str(pid) + "\"}"
            msg_json = jsonutils.create_log_json("PII", "PUT", json.loads(msg))
            msg_json['error'] = 'Not Found: ' + request.url
            self.logger.error("PII PUT " + json.dumps(msg_json))
            return rs_handlers.not_found(msg_json)

        tmp_dataset = json.loads(json.dumps(pii_dataset.__dict__))
        auth_pass = self.check_id(auth_resp, tmp_dataset)

        if not (auth_pass):
            return jsonutils.create_auth_fail_message()

        pii_dataset = datasetutils.update_pii_dataset_from_json(pii_dataset, in_json)
        currenttime = datetime.datetime.now()
        currenttime = currenttime.strftime("%Y/%m/%dT%H:%M:%S")
        pii_dataset.set_last_modified_date(currenttime)

        # update pii_dataset's non_pii_uuid
        non_pii_uuid_from_dataset = pii_dataset.get_uuid()
        try:
            non_pii_uuid = in_json[cfg.FIELD_PROFILE_UUID]
            is_non_pii_uuid_in_json_new = True
            # check if non-pii-uuid is already in there
            for i in range(len(non_pii_uuid_from_dataset)):
                if non_pii_uuid == non_pii_uuid_from_dataset[i]:
                    is_non_pii_uuid_in_json_new = False

            # adde non-pii uuid in json only if it is now uuid
            if is_non_pii_uuid_in_json_new:
                non_pii_uuid_from_dataset.append(non_pii_uuid)
                pii_dataset.set_non_pii_uuid(non_pii_uuid)
        except:
            pass

        result, pii_dataset = mongoutils.update_pii_dataset_in_mongo_by_field(cfg.FIELD_PID, pid,
                                                                              pii_dataset)

        if result is None:
            msg = "{\"reason\": \"Failed to update non pii uuid into pii dataset: " + str(pid) + "\"}"
            msg_json = jsonutils.create_log_json("PII", "PUT", json.loads(msg))
            msg_json['error'] = 'Not Implemented: ' + request.url
            self.logger.error("PII PUT " + json.dumps(msg_json))
            return rs_handlers.not_implemented(msg_json)

        pii_dataset = jsonutils.remove_file_descriptor_from_dataset(pii_dataset)
        out_json = mongoutils.construct_json_from_query_list(pii_dataset)
        msg_json = jsonutils.create_log_json("PII", "PUT", jsonutils.remove_objectid_from_dataset(pii_dataset))
        self.logger.info("PII PUT " + json.dumps(jsonutils.remove_objectid_from_dataset(msg_json)))
        return out_json

    def delete(self, pid):
        auth_resp = auth_middleware.authenticate()

        data_list, is_objectid, is_error, resp = self.get_data_list(pid)
        if is_error:
            return resp

        auth_pass = self.check_id(auth_resp, data_list[0])

        if not (auth_pass):
            return jsonutils.create_auth_fail_message()

        if (is_objectid):
            mongoutils.db_pii.pii_collection.delete_one({cfg.FIELD_OBJECTID: id})
            msg = "{\"pid\": \"" + str(pid) + "\"}"
            msg_json = jsonutils.create_log_json("PII", "DELETE", json.loads(msg))
            self.logger.info("PII DELETE " + json.dumps(msg_json))

            return rs_handlers.entry_deleted('pid', id)

        try:
            mongoutils.db_pii.pii_collection.delete_one({cfg.FIELD_PID: pid})
            msg = "{\"pid\": \"" + str(pid) + "\"}"
            msg_json = jsonutils.create_log_json("PII", "DELETE", json.loads(msg))
            self.logger.info("PII DELETE " + json.dumps(msg_json))
            return rs_handlers.entry_deleted('pid', pid)
        except:
            msg = "{\"reason\": \"failed to deleted pii. not found: " + str(pid) + "\"}"
            msg_json = jsonutils.create_log_json("PII", "DELETE", json.loads(msg))
            msg_json['error'] = 'Not Found: ' + request.url
            self.logger.info("PII DELETE " + json.dumps(msg_json))
            return rs_handlers.not_found(msg_json)


# TODO revive this when it needed
#  the following method is commented out for now but should be here for future use
# """
# upload image for the profile
# """
# class UploadProfileImage(Resource):
#     # TODO add unsupported media type handler
#     def __init__(self, **kwargs):
#         self.logger = kwargs.get('logger')
#
#     def post(self, pid):
#         pii_dataset = mongoutils.get_pii_dataset_from_field(cfg.FIELD_PID, pid)
#         if pii_dataset is None:
#             msg = "the pii dataset does not exist: " + str(pid)
#             self.logger.error(msg)
#             return rs_handlers.not_found(msg)
#
#         # create FileDescriptor for uploaded file
#         if 'file' not in request.files:
#             flash('No file part')
#             return redirect(request.url)
#
#         file = request.files['file']
#
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
#
#         fd = create_file_descriptor(cfg.PROFILE_REST_STORAGE, file)
#         file_descriptors = pii_dataset.get_file_descriptors()
#         if file_descriptors is None:
#             file_descriptors = []
#
#         file_descriptors.append(fd)
#         pii_dataset.set_file_descriptors(file_descriptors)
#         pii_dataset.set_image_url(fd.dataURL)
#         currenttime = datetime.datetime.now()
#         currenttime = currenttime.strftime("%Y/%m/%dT%H:%M:%S")
#         pii_dataset.set_last_modified_date(currenttime)
#
#         result, pii_dataset = mongoutils.update_pii_dataset_in_mongo_by_field(cfg.FIELD_PID, pid, pii_dataset)
#
#         if (result):
#             pii_dataset = jsonutils.remove_file_descriptor_from_dataset(pii_dataset)
#             out_json = mongoutils.construct_json_from_query_list(pii_dataset)
#             msg = "image has been posted to pii: " + str(pid)
#             self.logger.debug(msg)
#
#             return out_json
#         else:
#             msg = "Image update failed: " + str(pid)
#             self.logger.error(msg)
#             return rs_handlers.bad_request(msg)

log = logging.getLogger('werkzeug')
log.disabled = True

logging.Formatter.converter = gmtime
logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%dT%H:%M:%S',
                    format='%(asctime)-15s.%(msecs)03dZ %(levelname)-7s [%(threadName)-10s] : %(name)s - %(message)s')

endpoint_prefix = cfg.PROFILE_ENDPOINT

api.add_resource(NonPiiRootDir, endpoint_prefix, endpoint='non_pii_root',
                 resource_class_kwargs={'logger': logging.getLogger('profile_building_block')
                                        })
api.add_resource(DealNonPii, endpoint_prefix + '/<uuid>', endpoint='deal_non_pii',
                 resource_class_kwargs={'logger': logging.getLogger('profile_building_block')
                                        })
api.add_resource(PiiRootDir, endpoint_prefix + '/pii', endpoint='pii_root',
                 resource_class_kwargs={'logger': logging.getLogger('profile_building_block')
                                        })
api.add_resource(DealPii, endpoint_prefix + '/pii/<pid>', endpoint='deal_pii',
                 resource_class_kwargs={'logger': logging.getLogger('profile_building_block')
                                        })

# TODO this should be uncommneted when this needed
# api.add_resource(UploadProfileImage, '/profiles/pii/<pid>/uploadImage', endpoint='upload_profile_image',
#                  resource_class_kwargs={'logger': logging.getLogger('profileservice')
#                                         })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
