"""
author: Yong Wook Kim (NCSA ywkim@illinois.edu)
created 2019 Apr 5
"""
# !flask/bin/python
import logging
import flask
import json
import uuid

import profileservice.restservice.utils.mongoutils as mongoutils
import profileservice.configs as cfg

from bson import ObjectId
from flask import flash, redirect, jsonify, make_response, request
from bson.json_util import dumps
from profileservice.dao.pii_data import pii_data
from profileservice.dao.non_pii_data import non_pii_data
from profileservice.restservice.utils.otherutils import create_file_descriptor

app = flask.Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

__logger = logging.getLogger("rokwire-building-blocks-api")

"""
rest service for root directory
"""
@app.route('/profiles', methods=['GET', 'POST'])
def root_dir():
    if request.method == 'GET':
        db_data = mongoutils.db.non_pii_collection.find({}, {'_id': False})
        data_list = list(db_data)

        out_json = mongoutils.construct_json_from_query_list(data_list)
        logging.debug("list all profiles")

        return out_json

    elif request.method == 'POST':
        in_json = request.get_json()
        # check if uuid is in there otherwise it is a bad request
        non_pii_uuid = in_json["uuid"]
        if len(non_pii_uuid) > 0:
            # get dataset using uuid
            dataset = mongoutils.get_non_pii_dataset_from_field('uuid', non_pii_uuid)
            if dataset is None:
                msg = "the dataset does not exist with uuid of : " + str(non_pii_uuid)
                logging.error(msg)
                return not_found()
            else:
                # the process in here is that, uuid(non-pii-id) will be recorded in pii entry
                # to do this, it must check if there is a pii entry with given information
                # in here, the email is used but this should be updated to smarter way
                # TODO update pii etnry checking process smarter, not just using email

                # check if pii dataset for the given information exists
                pii_json = in_json["pii_data"]
                email = pii_json["email"]
                pii_dataset = mongoutils.get_pii_dataset_from_field('email', email)
                if pii_dataset is not None:
                    pii_uuid = pii_dataset.get_pii_uuid()
                    msg = "Requested uuid already has pii data of " + str(pii_uuid)
                    logging.debug(msg)

                    # update pii_dataset's non_pii_uuid
                    non_pii_uuid_in_pii = pii_dataset.get_non_pii_uuid()
                    if non_pii_uuid_in_pii is None:
                        non_pii_uuid_in_pii = []
                    non_pii_uuid_in_pii.append(non_pii_uuid)

                    pii_dataset.set_non_pii_uuid(non_pii_uuid_in_pii)

                    result, pii_dataset = mongoutils.update_pii_dataset_in_mongo_by_field('pii_uuid', pii_uuid,
                                                                                              pii_dataset)

                    if result is None:
                        msg = "Failed to update non pii uuid into pii dataset: " + str(pii_uuid)
                        logging.debug(msg)

                        return not_implemented()
                else:
                    # insert new pii_dataset
                    pii_dataset = pii_data(pii_json)
                    pii_uuid = str(uuid.uuid4())
                    pii_dataset.set_pii_uuid(pii_uuid)
                    non_pii_uuid_in_pii =[]
                    non_pii_uuid_in_pii.append(non_pii_uuid)
                    pii_dataset.set_non_pii_uuid(non_pii_uuid_in_pii)
                    result = mongoutils.insert_pii_dataset_to_mongodb(pii_dataset)

                    if result is None:
                        msg = "Failed to update non pii uuid into pii dataset: " + str(pii_uuid)
                        logging.debug(msg)

                        return not_implemented()

                # create pii data first and save it in the pii collection then get the unique id of pii data
                non_pii_dataset = non_pii_data(in_json)

                # update non_pii object
                result, dataset = mongoutils.update_non_pii_dataset_in_mongo_by_field('uuid', non_pii_uuid, non_pii_dataset)

                if (result):
                    out_json = mongoutils.construct_json_from_query_list(dataset)
                    msg = "New profile has been posted with : " + str(non_pii_uuid)
                    logging.debug(msg)

                    return out_json
                else:
                    return bad_request()
        else:
            msg = "uuid " + str(non_pii_uuid) + " not found"
            logging.error(msg)
            return not_found()
    else:
        logging.error("list profile dataset failed.")
        return bad_request()


"""
post a new record to get non-pii (when new app get installed
"""
@app.route('/profiles/non-pii', methods=['POST'])
def new_app_installation():
    if request.method == 'POST':
        non_pii_dataset = non_pii_data('')
        dataset, id = mongoutils.insert_non_pii_dataset_to_mongodb(non_pii_dataset)
        uuid = dataset["uuid"]
        outstr = "{\"uuid\": \"%s\"}" % (uuid)
        outjson = json.loads(outstr)
        data_dump = dumps(outjson)
        out_json = make_response(data_dump)
        out_json.mimetype = 'application/json'

        msg = "new profile with new uuid has been created: " + str(uuid)
        logging.debug(msg)

        return out_json

    else:
        bad_request()

        return None


"""
provide profile information by profile id or remove it
"""
@app.route('/profiles/<uuid>', methods=['GET', 'DELETE'])
def deal_profile_id(uuid):
    if uuid != None:
        is_objectid = mongoutils.check_if_objectid(uuid)

        # query using either non-pii ObjectId or uuid
        if (is_objectid):
            id = ObjectId(uuid)
            db_data = mongoutils.query_non_pii_dataset_by_objectid(id)
        else:
            db_data = mongoutils.query_non_pii_dataset('uuid', uuid)

        data_list = list(db_data)
        if len(data_list) > 0:
            out_json = mongoutils.construct_json_from_query_list(data_list)

            if request.method == 'GET':
                msg = "request profile information: " + str(uuid)
                logging.debug(msg)

            # delete profile by using profile id
            if request.method == 'DELETE':
                if (is_objectid):
                    mongoutils.db.non_pii_collection.delete_one({'_id': id})
                    msg = "deleted profile information: " + str(uuid)
                    logging.debug(msg)
                    return entry_deleted()
                else:
                    try:
                        mongoutils.db.non_pii_collection.delete_one({'uuid': uuid})
                        msg = "deleted profile information: " + str(uuid)
                        logging.debug(msg)
                        return entry_deleted()
                    except:
                        msg = "failed to deleted. not found: " + str(uuid)
                        logging.error(msg)
                        return not_found()

            return out_json
        else:
            msg = "the dataset does not exist: " + str(uuid)
            logging.error(msg)
            return not_found()
    else:
        return bad_request()


"""
provide profile information by profile id or remove it
"""
@app.route('/profiles/<uuid>/uploadImage', methods=['POST'])
def upload_profile_image(uuid):
    # TODO add unsupported media type handler
    if request.method == 'POST':
        non_pii_dataset = mongoutils.get_non_pii_dataset_from_field('uuid', uuid)
        if non_pii_dataset is None:
            msg = "the dataset does not exist: " + str(uuid)
            logging.error(msg)
            return not_found()
        else:
            # create FileDescriptor for uploaded file
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)

            file = request.files['file']

            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)

            fd = create_file_descriptor(cfg.PROFILE_REST_STORAGE, file)
            file_descriptors = non_pii_dataset.get_file_descriptors()
            if file_descriptors is None:
                file_descriptors = []
            file_descriptors.append(fd)
            non_pii_dataset.set_file_descriptors(file_descriptors)
            non_pii_dataset.set_image_uri(fd.dataURL)

            result, non_pii_dataset = mongoutils.update_non_pii_dataset_in_mongo_by_field('uuid', uuid, non_pii_dataset)

            if (result):
                out_json = mongoutils.construct_json_from_query_list(non_pii_dataset)
                msg = "image has been posted to: " + str(uuid)
                logging.debug(msg)

                return out_json
            else:
                return bad_request()
    else:
        return bad_request()

@app.route('/profiles/pii', methods=['GET'])
def pii_root_dir():
    if request.method == 'GET':
        term_uuid = request.args.get('uuid', None)
        term_username = request.args.get('username', None)
        term_phone = request.args.get('phone', None)
        term_email = request.args.get('email', None)

        # TODO this if else method should smarter like case or something else
        if term_uuid != None:
            out_json = mongoutils.get_pii_http_output_query_result_using_field_string('pii_uuid', term_uuid)
            if out_json == None:
                return not_found()
            else:
                return out_json
        if term_username != None:
            out_json = mongoutils.get_pii_http_output_query_result_using_field_string('username', term_username)
            if out_json == None:
                return not_found()
            else:
                return out_json
        if term_phone != None:
            out_json = mongoutils.get_pii_http_output_query_result_using_field_string('phone', term_phone)
            if out_json == None:
                return not_found()
            else:
                return out_json
        if term_email != None:
            out_json = mongoutils.get_pii_http_output_query_result_using_field_string('email', term_email)
            if out_json == None:
                return not_found()
            else:
                return out_json

        else:
            db_data = mongoutils.db.pii_collection.find({}, {'_id': False})
            data_list = list(db_data)

        out_json = mongoutils.construct_json_from_query_list(data_list)
        logging.debug("list all pii data")

        return out_json
    else:
        logging.error("list pii dataset failed.")
        return bad_request()

"""
provide profile information by profile id or remove it
"""
@app.route('/profiles/pii/<uuid>', methods=['GET', 'DELETE'])
def deal_pii_id(uuid):
    if uuid != None:
        is_objectid = mongoutils.check_if_objectid(uuid)

        # query using either non-pii ObjectId or uuid
        if (is_objectid):
            id = ObjectId(uuid)
            db_data = mongoutils.query_pii_dataset_by_objectid(id)
        else:
            db_data = mongoutils.query_pii_dataset('pii_uuid', uuid)

        data_list = list(db_data)
        if len(data_list) > 0:
            out_json = mongoutils.construct_json_from_query_list(data_list)

            if request.method == 'GET':
                msg = "request profile information: " + str(uuid)
                logging.debug(msg)

            # delete profile by using profile id
            if request.method == 'DELETE':
                if (is_objectid):
                    mongoutils.db.pii_collection.delete_one({'_id': id})
                    msg = "deleted pii information: " + str(uuid)
                    logging.debug(msg)

                    return entry_deleted()
                else:
                    try:
                        mongoutils.db.pii_collection.delete_one({'pii_uuid': uuid})
                        msg = "deleted pii information: " + str(uuid)
                        logging.debug(msg)

                        return entry_deleted()
                    except:
                        msg = "failed to deleted pii. not found: " + str(uuid)
                        logging.error(msg)
                    return not_found()

            return out_json
        else:
            msg = "the pii dataset does not exist: " + str(uuid)
            logging.error(msg)
            return not_found()
    else:
        return bad_request()

"""
make reponse for handling 202 entry deleted
"""
def entry_deleted(id):
    message = {
        'status': 202,
        'message': 'Object is deleted with id of : ' + id,
    }
    resp = jsonify(message)
    resp.status_code = 202

    return make_response(resp)


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

@app.errorhandler(500)
def internal_server_error(error=None):
    message = {
        'status': 500,
        'message': 'Internal Server Error: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 500

    return resp

@app.errorhandler(501)
def not_implemented(error=None):
    message = {
        'status': 501,
        'message': 'Not Implemented: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 501

    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
