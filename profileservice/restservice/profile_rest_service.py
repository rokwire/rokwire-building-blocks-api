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

__logger = logging.getLogger("profileservice")

"""
rest service for root directory
"""
@app.route('/profiles', methods=['GET', 'POST'])
def non_pii_root_dir():
    if request.method == 'GET':
        db_data = mongoutils.db.non_pii_collection.find({}, {'_id': False})
        data_list = list(db_data)

        out_json = mongoutils.construct_json_from_query_list(data_list)
        logging.debug("list all profiles")

        return out_json

    elif request.method == 'POST':
        in_json = request.get_json()
        # check if uuid is in there otherwise it is either a first installation
        is_new_install = False
        try:
            non_pii_uuid = in_json["uuid"]
            # even if there is non_pii_uuid is in the input json, it could be a new one
            # check if the dataset is existing with given uuid
            dataset = mongoutils.get_non_pii_dataset_from_field('uuid', non_pii_uuid)
            if dataset is None:
                is_new_install = True
        except:
            is_new_install = True

        if is_new_install:
            # new installation of the app
            non_pii_dataset = non_pii_data('')
            dataset, id = mongoutils.insert_non_pii_dataset_to_mongodb(non_pii_dataset)
            profile_uuid = dataset["uuid"]
            out_json = mongoutils.construct_json_from_query_list(dataset)
            msg = "new profile with new uuid has been created: " + str(profile_uuid)
            logging.debug(msg)

            return out_json
        else:
            # updated non-pii profile data with given uuid
            if len(non_pii_uuid) > 0:
                # get dataset using uuid
                dataset = mongoutils.get_non_pii_dataset_from_field('uuid', non_pii_uuid)
                if dataset is None:
                    msg = "the dataset does not exist with uuid of : " + str(non_pii_uuid)
                    logging.error(msg)
                    return not_found()
                else:
                    # TODO check the app that the app should post cached data fully to the endpoint
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

# """
# post a new record to get non-pii (when new app get installed
# """
# @app.route('/profiles/non-pii', methods=['POST'])
# def new_app_installation():
#     if request.method == 'POST':
#         non_pii_dataset = non_pii_data('')
#         dataset, id = mongoutils.insert_non_pii_dataset_to_mongodb(non_pii_dataset)
#         uuid = dataset["uuid"]
#         outstr = "{\"uuid\": \"%s\"}" % (uuid)
#         outjson = json.loads(outstr)
#         data_dump = dumps(outjson)
#         out_json = make_response(data_dump)
#         out_json.mimetype = 'application/json'
#
#         msg = "new profile with new uuid has been created: " + str(uuid)
#         logging.debug(msg)
#
#         return out_json
#
#     else:
#         bad_request()
#
#         return None


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
upload image for the profile
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

""""
get or post pii dataset
"""
@app.route('/profiles/pii', methods=['GET', 'POST'])
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
    elif request.method == 'POST':
        in_json = request.get_json()

        # get uuid, if failed it is a bad request
        try:
            non_pii_uuid = in_json["uuid"]
        except:
            bad_request()

        # check if it is a new record or existing record
        is_new_entry = False
        try:
            pii_uuid = in_json["pii_uuid"]
        except:
            is_new_entry = True

        pii_dataset = pii_data(in_json)
        if is_new_entry:
            # insert new pii_dataset
            pii_uuid = str(uuid.uuid4())
            pii_dataset.set_pii_uuid(pii_uuid)
            non_pii_uuid_from_dataset = []
            non_pii_uuid_from_dataset.append(non_pii_uuid)
            pii_dataset.set_non_pii_uuid(non_pii_uuid_from_dataset)
            result = mongoutils.insert_pii_dataset_to_mongodb(pii_dataset)

            if result is None:
                msg = "Failed to update non pii uuid into pii dataset: " + str(pii_uuid)
                logging.error(msg)

                return not_implemented()
            else:
                out_json = mongoutils.construct_json_from_query_list(result)
                msg = "Pii data has been posted with : " + str(pii_uuid)
                logging.debug(msg)

                return out_json
        else:
            # TODO check the app that the app should post cached data fully to the endpoint
            # if pii_uuid is none or the lenght is zero, then it is not right
            if pii_uuid is None or len(pii_uuid) == 0:
                return not_found()
            # check if the pii_uuid is really existing in the database
            pii_dataset = mongoutils.get_pii_dataset_from_field('pii_uuid', pii_uuid)

            if pii_dataset == None:
                return not_found()
            else:
                msg = "Pii data will be updated with the id of " + str(pii_uuid)
                logging.debug(msg)

                # update pii_dataset's non_pii_uuid
                non_pii_uuid_from_dataset = pii_dataset.get_non_pii_uuid()
                is_non_pii_uuid_in_json_new = True
                if non_pii_uuid_from_dataset is None:
                    non_pii_uuid_from_dataset = []
                else:   # check if non-pii-uuid is already in there
                    for i in range(len(non_pii_uuid_from_dataset)):
                        if non_pii_uuid == non_pii_uuid_from_dataset[i]:
                            is_non_pii_uuid_in_json_new = False

                # adde non-pii uuid in json only if it is now uuid
                if is_non_pii_uuid_in_json_new:
                    non_pii_uuid_from_dataset.append(non_pii_uuid)

                pii_dataset.set_non_pii_uuid(non_pii_uuid)

                result, pii_dataset = mongoutils.update_pii_dataset_in_mongo_by_field('pii_uuid', pii_uuid,
                                                                                      pii_dataset)

                if result is None:
                    msg = "Failed to update non pii uuid into pii dataset: " + str(pii_uuid)
                    logging.error(msg)

                    return not_implemented()
                else:
                    out_json = mongoutils.construct_json_from_query_list(pii_dataset)
                    msg = "Pii data has been posted with : " + str(pii_uuid)
                    logging.debug(msg)

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
