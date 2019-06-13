import sys
sys.path.append('../../')
import datetime
import logging
import uuid as uuidlib

from flask import Flask, flash, redirect, request
from flask_restful import Resource, Api
from bson import ObjectId

import profileservice.configs as cfg
import profileservice.restservice.utils.mongoutils as mongoutils
import profileservice.restservice.utils.jsonutils as jsonutils
import profileservice.restservice.utils.datasetutils as datasetutils
import profileservice.restservice.utils.rest_handlers as rs_handlers

from profileservice import middleware
from profileservice.dao.pii_data import pii_data
from profileservice.dao.non_pii_data import non_pii_data
from profileservice.restservice.utils.otherutils import create_file_descriptor

app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False
# app.before_request(middleware.authenticate)

__logger = logging.getLogger("profileservice")

mongoutils.index_non_pii_data()
mongoutils.index_pii_data()

"""
profile rest service root directory
"""
class NonPiiRootDir(Resource):
    def post(self):
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
                msg = "UUID in input json already exists in the database " + str(non_pii_uuid)
                logging.error(msg)
                return rs_handlers.bad_request(msg)
        except:
            pass

        if is_new_install:
            # new installation of the app
            currenttime = datetime.datetime.now()
            currenttime = currenttime.strftime("%Y/%m/%dT%H:%M:%S")
            non_pii_dataset = non_pii_data('')
            non_pii_uuid = str(uuidlib.uuid4())
            non_pii_dataset.set_uuid(non_pii_uuid)
            non_pii_dataset.set_creation_date(currenttime)
            non_pii_dataset.set_last_modified_date(currenttime)
            dataset, id = mongoutils.insert_non_pii_dataset_to_mongodb(non_pii_dataset)
            profile_uuid = dataset["uuid"]
            dataset = jsonutils.remove_objectid_from_dataset(dataset)

            out_json = mongoutils.construct_json_from_query_list(dataset)
            msg = "new profile with new uuid has been created: " + str(profile_uuid)
            logging.debug(msg)

            return rs_handlers.return_id(msg, 'uuid', profile_uuid)

"""
provide profile information by profile id or remove it
"""
class DealNonPii(Resource):
    def get_data_list(self, uuid):
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
                return rs_handlers.bad_request('There are more than 1 record')

            if len(data_list) == 0:
                return rs_handlers.bad_request('There is no record for the uuid')

            return data_list, is_objectid

        else:
            msg = "the dataset does not exist: " + str(uuid)
            logging.error(msg)
            return rs_handlers.not_found("Profile not found")

    def get(self, uuid):
        msg = "request profile information: " + str(uuid)
        logging.debug(msg)

        data_list, is_objectid = self.get_data_list(uuid)

        out_json = mongoutils.construct_json_from_query_list(data_list[0])

        return out_json

    def put(self, uuid):
        try:
            in_json = request.get_json()
        except:
            return rs_handlers.bad_request('json format error')

        # check if the uuid is really existing in the database
        non_pii_dataset = mongoutils.get_non_pii_dataset_from_field(cfg.FIELD_PROFILE_UUID, uuid)

        if non_pii_dataset is None:
            msg = "There is no profile dataset with given uuid " + str(uuid)
            logging.error(msg)
            return rs_handlers.not_found("Profile not found")

        msg = "Profile data will be updated with the id of " + str(uuid)
        logging.debug(msg)

        non_pii_dataset = datasetutils.update_non_pii_dataset_from_json(non_pii_dataset, in_json)
        currenttime = datetime.datetime.now()
        currenttime = currenttime.strftime("%Y/%m/%dT%H:%M:%S")
        non_pii_dataset.set_last_modified_date(currenttime)

        result, non_pii_dataset = mongoutils.update_non_pii_dataset_in_mongo_by_field(
            cfg.FIELD_PROFILE_UUID, uuid,
            non_pii_dataset)

        if result is None:
            msg = "Failed to update non Profile dataset: " + str(uuid)
            logging.error(msg)

            return rs_handlers.not_implemented("Invalid ID supplied")

        non_pii_dataset = jsonutils.remove_file_descriptor_from_dataset(non_pii_dataset)
        out_json = mongoutils.construct_json_from_query_list(non_pii_dataset)
        msg = "Profile data has been posted with : " + str(uuid)
        logging.debug(msg)

        return out_json

    def delete(self, uuid):
        data_list, is_objectid = self.get_data_list(uuid)

        if (is_objectid):
            mongoutils.db_profile.non_pii_collection.delete_one({cfg.FIELD_OBJECTID: id})
            msg = "deleted profile information: " + str(id)
            logging.debug(msg)
            return rs_handlers.entry_deleted(id)

        try:
            mongoutils.db_profile.non_pii_collection.delete_one({cfg.FIELD_PROFILE_UUID: uuid})
            msg = "deleted profile information: " + str(uuid)
            logging.debug(msg)
            return rs_handlers.entry_deleted(uuid)
        except:
            msg = "failed to deleted. the dataset does not exist: " + str(uuid)
            logging.error(msg)
            return rs_handlers.not_found("Profile not found")

""""
get or post pii dataset
"""
class PiiRootDir(Resource):
    def get(self):
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
        is_new_entry = False
        try:
            in_json = request.get_json()
        except:
            return rs_handlers.bad_request('json format error')

        # get uuid, if failed it is a bad request
        try:
            non_pii_uuid = in_json[cfg.FIELD_PROFILE_UUID]
        except:
            return rs_handlers.bad_request('Invalid ID supplied')

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
                return rs_handlers.return_id('The email already exists.', 'pid', pid)
        except:
            pass

        # check if the phonenumber already exists
        try:
            phone = in_json['phone']
            dataset = mongoutils.get_pii_dataset_from_field('phone', phone)
            if dataset is not None:
                pid = dataset.get_pid()
                return rs_handlers.return_id('Phone number already exists.', 'pid', pid)
        except:
            pass

        if dataset is not None:
            is_new_entry = False

        pii_dataset = pii_data(in_json)

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
                msg = "Failed to update non pii uuid into pii dataset: " + str(pid)
                logging.error(msg)

                return rs_handlers.not_implemented("Invalid ID supplied")

            msg = "Pii data has been posted with : " + str(pid)
            logging.debug(msg)

            return rs_handlers.return_id(msg, 'pid', pid)
        else:
            msg = 'The request is wrong or the entry already exists'
            logging.error(msg)

            return rs_handlers.bad_request("Invalid ID supplied")

"""
provide profile information by profile id or remove it
"""
class DealPii(Resource):
    def get_data_list(self, pid):
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
                return rs_handlers.bad_request('There are more than 1 record')

            if len(data_list) == 0:
                return rs_handlers.bad_request('There is no record for the uuid')

            if len(data_list) > 0:
                return data_list, is_objectid

        else:
            msg = "the pii dataset does not exist: " + str(pid)
            logging.error(msg)
            return rs_handlers.not_found("Pii entry not found")

    def get(self, pid):
        msg = "request profile information: " + str(pid)
        logging.debug(msg)

        data_list, is_objectid = self.get_data_list(pid)

        # remove fileDescriptors from db_data
        data_list = jsonutils.remove_file_descriptor_from_data_list(data_list)
        out_json = mongoutils.construct_json_from_query_list(data_list[0])

        return out_json

    def put(self, pid):
        try:
            in_json = request.get_json()
        except:
            return rs_handlers.bad_request('json format error')

        # check if the pid is really existing in the database
        pii_dataset = mongoutils.get_pii_dataset_from_field(cfg.FIELD_PID, pid)

        if pii_dataset == None:
            msg = "There is no dataset with given pii uuid " + str(pid)
            logging.error(msg)
            return rs_handlers.not_found("Profile not found")

        msg = "Pii data will be updated with the id of " + str(pid)
        logging.debug(msg)

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
            msg = "Failed to update non pii uuid into pii dataset: " + str(pid)
            logging.error(msg)

            return rs_handlers.not_implemented("Invalid ID supplied")

        pii_dataset = jsonutils.remove_file_descriptor_from_dataset(pii_dataset)
        out_json = mongoutils.construct_json_from_query_list(pii_dataset)
        msg = "Pii data has been posted with : " + str(pid)
        logging.debug(msg)

        return out_json

    def delete(self, pid):
        data_list, is_objectid = self.get_data_list(pid)

        if (is_objectid):
            mongoutils.db_pii.pii_collection.delete_one({cfg.FIELD_OBJECTID: id})
            msg = "deleted pii information: " + str(pid)
            logging.debug(msg)

            return rs_handlers.entry_deleted(id)

        try:
            mongoutils.db_pii.pii_collection.delete_one({cfg.FIELD_PID: pid})
            msg = "deleted pii information: " + str(pid)
            logging.debug(msg)
            return rs_handlers.entry_deleted(pid)
        except:
            msg = "failed to deleted pii. not found: " + str(pid)
            logging.error(msg)
            return rs_handlers.not_found("Profile not found")

# TODO revive this when it needed
#  the following method is commented out for now but should be here for future use
"""
upload image for the profile
"""
class UploadProfileImage(Resource):
    # TODO add unsupported media type handler
    def post(self, pid):
        pii_dataset = mongoutils.get_pii_dataset_from_field(cfg.FIELD_PID, pid)
        if pii_dataset is None:
            msg = "the dataset does not exist: " + str(pid)
            logging.error(msg)
            return rs_handlers.not_found()

        # create FileDescriptor for uploaded file
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        fd = create_file_descriptor(cfg.PROFILE_REST_STORAGE, file)
        file_descriptors = pii_dataset.get_file_descriptors()
        if file_descriptors is None:
            file_descriptors = []

        file_descriptors.append(fd)
        pii_dataset.set_file_descriptors(file_descriptors)
        pii_dataset.set_image_url(fd.dataURL)
        currenttime = datetime.datetime.now()
        currenttime = currenttime.strftime("%Y/%m/%dT%H:%M:%S")
        pii_dataset.set_last_modified_date(currenttime)

        result, pii_dataset = mongoutils.update_pii_dataset_in_mongo_by_field(cfg.FIELD_PID, pid, pii_dataset)

        if (result):
            pii_dataset = jsonutils.remove_file_descriptor_from_dataset(pii_dataset)
            out_json = mongoutils.construct_json_from_query_list(pii_dataset)
            msg = "image has been posted to: " + str(pid)
            logging.debug(msg)

            return out_json
        else:
            return rs_handlers.bad_request('dataset update to db failed')

api.add_resource(NonPiiRootDir, '/profiles', endpoint='non_pii_root')
api.add_resource(DealNonPii, '/profiles/<uuid>', endpoint='deal_non_pii')
api.add_resource(PiiRootDir, '/profiles/pii', endpoint='pii_root')
api.add_resource(DealPii, '/profiles/pii/<pid>', endpoint='deal_pii')

#TODO this should be uncommneted when this needed
api.add_resource(UploadProfileImage, '/profiles/pii/<pid>/uploadImage', endpoint='upload_profile_image')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)