"""
author: Yong Wook Kim (NCSA ywkim@illinois.edu)
created 2019 Apr 5
"""
# !flask/bin/python
import logging
import flask
import json

import profileservice.restservice.utils.mongoutils as mongoutils
import profileservice.configs as cfg

from bson import ObjectId
from flask import flash, redirect, jsonify, make_response, request
from bson.json_util import dumps
from profileservice.dao.profiledataset import ProfileDataset
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
        term_npid = request.args.get('uuid', None)
        term_netid = request.args.get('netid', None)
        term_phone = request.args.get('phone', None)
        term_email = request.args.get('email', None)

        # TODO this if else method should smarter like case or something else
        if term_npid != None:
            out_json = mongoutils.get_http_output_query_result_using_field_string('uuid', term_npid)
            if out_json == None:
                return not_found()
            else:
                return out_json
        if term_netid != None:
            out_json = mongoutils.get_http_output_query_result_using_field_string('pii_data.netid', term_netid)
            if out_json == None:
                return not_found()
            else:
                return out_json
        if term_phone != None:
            out_json = mongoutils.get_http_output_query_result_using_field_string('pii_data.phonenumber', term_phone)
            if out_json == None:
                return not_found()
            else:
                return out_json
        if term_email != None:
            out_json = mongoutils.get_http_output_query_result_using_field_string('pii_data.email', term_email)
            if out_json == None:
                return not_found()
            else:
                return out_json

        else:
            db_data = mongoutils.db.collection.find({})  # db.collection.find({}, {'_id': False})
            data_list = list(db_data)

        out_json = mongoutils.construct_json_from_query_list(data_list)
        logging.debug("list all profiles")

        return out_json

    elif request.method == 'POST':
        in_json = request.get_json()
        # check if uuid is in there otherwise it is a bad request
        uuid = in_json["uuid"]
        if len(uuid) > 0:
            # get dataset using uuid
            dataset = mongoutils.get_query_dataset_from_field('uuid', uuid)
            if dataset is None:
                msg = "the dataset does not exist with uuid of : " + str(uuid)
                logging.error(msg)
                return not_found()
            else:
                # create profile object
                profile = ProfileDataset(in_json)
                result, dataset = mongoutils.update_dataset_in_mongo_by_field('uuid', uuid, profile)

                if (result):
                    out_json = mongoutils.construct_json_from_query_list(dataset)
                    msg = "New profile has been posted with : " + str(uuid)
                    logging.debug(msg)

                    return out_json
                else:
                    return bad_request()
        else:
            msg = "uuid " + str(uuid) + " not found"
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
        profile = ProfileDataset('')
        dataset, id = mongoutils.insert_profile_to_mongodb(profile)
        profile_id = dataset["uuid"]
        outstr = "{\"profile_id\": \"%s\"}" % (profile_id)
        outjson = json.loads(outstr)
        data_dump = dumps(outjson)
        out_json = make_response(data_dump)
        out_json.mimetype = 'application/json'

        msg = "new profile id has been created: " + str(profile_id)
        logging.debug(msg)

        return out_json

    else:
        bad_request()

        return None


"""
provide profile information by profile id or remove it
"""
@app.route('/profiles/<objectId>', methods=['GET', 'DELETE'])
def deal_profile_id(objectId):
    if objectId != None:
        is_profile_id = mongoutils.check_if_objectid(objectId)

        # query using either profile id or user name
        if (is_profile_id):
            id = ObjectId(objectId)
            db_data = mongoutils.query_dataset_by_objectid(id)
        else:
            db_data = mongoutils.query_dataset('username', objectId)

        data_list = list(db_data)
        if len(data_list) > 0:
            out_json = mongoutils.construct_json_from_query_list(data_list)

            if request.method == 'GET':
                msg = "request profile information: " + str(objectId)
                logging.debug(msg)

            # delete profile by using profile id
            if request.method == 'DELETE':
                if (is_profile_id):
                    mongoutils.db.collection.delete_one({'_id': id})
                    msg = "deleted profile information: " + str(objectId)
                    logging.debug(msg)
                else:
                    msg = "failed to deleted. not found: " + str(objectId)
                    logging.error(msg)
                    return not_found()

            return out_json
        else:
            msg = "the dataset does not exist: " + str(objectId)
            logging.error(msg)
            return not_found()
    else:
        return bad_request()


"""
provide profile information by profile id or remove it
"""
@app.route('/profiles/<objectid>/uploadImage', methods=['POST'])
def upload_profile_image(objectid):
    # TODO add unsupported media type handler
    if request.method == 'POST':
        dataset = mongoutils.get_dataset_from_objectid(objectid)
        if dataset is None:
            msg = "the dataset does not exist: " + str(objectid)
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
            file_descriptors = dataset.get_file_descriptors()
            if file_descriptors is None:
                file_descriptors = []
            file_descriptors.append(fd)
            dataset.set_file_descriptors(file_descriptors)
            dataset.set_image_uri(fd.dataURL)

            result, dataset = mongoutils.update_dataset_in_mongo_by_objectid(objectid, dataset)

            if (result):
                out_json = mongoutils.construct_json_from_query_list(dataset)
                msg = "image has been posted to: " + str(objectid)
                logging.debug(msg)

                return out_json
            else:
                return bad_request()
    else:
        return bad_request()

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
