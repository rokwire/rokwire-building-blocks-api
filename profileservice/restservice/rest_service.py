"""
author: Yong Wook Kim
created 2019 Apr 5
"""
#!flask/bin/python
import hashlib
import logging
import urllib
from urllib.request import urlretrieve

import flask
import os
import json
import profileservice.configs as cfg

from mimetypes import MimeTypes
from bson import ObjectId
from flask import flash, redirect
from pymongo import MongoClient
from flask import make_response
from flask import request
from bson.json_util import dumps
from profileservice.dao.profiledataset import ProfileDataset
from profileservice.dao.filedescriptor import FileDescriptor
from profileservice.restservice.error_handler import not_found, bad_request, forbidden, unsupported_media_type

app = flask.Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

client = MongoClient(cfg.profile_mongo_url, connect=False)
db = client[cfg.profile_db_name]
db.collection = db[cfg.profile_db_coll_name]
__logger = logging.getLogger("rokwire-building-blocks-api")


"""
rest service for root directory
"""
@app.route('/profiles', methods = ['GET', 'POST'])
def root_dir():
    if request.method == 'GET':
        db_data = db.collection.find({}) #db.collection.find({}, {'_id': False})
        data_list = list(db_data)
        out_json = construct_json_from_query_list(data_list)
        logging.debug("list all profiles")

        return out_json

    elif request.method == 'POST':
        in_json = request.get_json()
        profile = ProfileDataset(in_json)
        dataset, id = insert_profile_to_mongodb(profile)
        out_json = construct_json_from_query_list(dataset)
        logging.debug("new profiles added: " + str(id))

        msg = "data has been posted: " + str(id)
        logging.debug(msg)

        return out_json

    else:
        logging.error("list profile dataset failed.")
        return bad_request()

"""
provide profile information by profile id or remove it
"""
@app.route('/profiles/<profileid>', methods = ['GET', 'DELETE'])
def deal_profile_id(profileid):
    if profileid != None:
        is_profile_id = check_if_objectid(profileid)

        # query using either profile id or user name
        if (is_profile_id):
            id = ObjectId(profileid)
            db_data = query_dataset_by_objectid(id)
        else:
            db_data = query_dataset('username', profileid)

        data_list = list(db_data)
        if len(data_list) > 0:
            out_json = construct_json_from_query_list(data_list)

            if request.method == 'GET':
                msg = "request profile information: " + str(profileid)
                logging.debug(msg)

            # delete profile by using profile id
            if request.method == 'DELETE':
                if (is_profile_id):
                    db.collection.delete_one({'_id':id})
                    msg = "deleted profile information: " + str(profileid)
                    logging.debug(msg)
                else:
                    msg = "failed to deleted. not found: " + str(profileid)
                    logging.error(msg)
                    return not_found()

            return out_json
        else:
            msg = "the dataset does not exist: " + str(profileid)
            logging.error(msg)
            return not_found()
    else:
        return bad_request()

"""
provide profile information by profile id or remove it
"""
@app.route('/profiles/<profileid>/uploadImage', methods = ['POST'])
def upload_profile_image(profileid):
    #TODO add unsupported media type handler
    if request.method == 'POST':
        dataset = get_dataset_from_objectid(profileid)
        if dataset is None:
            msg = "the dataset does not exist: " + str(profileid)
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

            fd = create_file_descriptor(cfg.profile_rest_storage, file)
            file_descriptors = dataset.get_file_descriptors()
            if file_descriptors is None:
                file_descriptors = []
            file_descriptors.append(fd)
            dataset.set_file_descriptors(file_descriptors)
            dataset.set_image_uri(fd.dataURL)

            result, dataset = update_dataset_in_mongo(profileid, dataset)

            if (result):
                out_json = construct_json_from_query_list(dataset)
                msg = "image has been posted to: " + str(profileid)
                logging.debug(msg)

                return out_json
            else:
                return bad_request()

"""
convert mongodb query result to profile object
"""
def get_dataset_from_objectid(profileid):
    is_profile_id = check_if_objectid(profileid)
    if is_profile_id:
        id = ObjectId(profileid)
        db_data = query_dataset_by_objectid(id)
        data_list = list(db_data)
        if len(data_list) > 0:
            data_dump = dumps(data_list)
            data_dump = data_dump[:-1]
            data_dump = data_dump[1:]
            json_load = json.loads(data_dump)
            dataset = ProfileDataset(json_load)

            return dataset
        else:
            return None
    else:
        return None

"""
check if the query string is objectid
"""
def check_if_objectid(query_str):
    is_objectid = True
    try:
        id = ObjectId(query_str)
    except:
        is_objectid = False

    return is_objectid

"""
query dataset using object id
"""
def query_dataset_by_objectid(objectid):
    return db.collection.find({'_id':objectid})

"""
qyery dataset using field
"""
def query_dataset(fld, query_str):
    return db.collection.find({fld: query_str})

"""
construct json from mongo query
"""
def construct_json_from_query_list(data_list):
    data_dump = dumps(data_list)
    out_json = make_response(data_dump)
    out_json.mimetype = 'application/json'

    return out_json

"""
insert profile json to mognodb
"""
def insert_profile_to_mongodb(indataset):
    dataset = json.dumps(indataset, default=lambda x: x.__dict__)
    dataset = json.loads(dataset)

    id = db.collection.insert(dataset)

    return dataset, id

"""
update profile dataset in mongodb
"""
def update_dataset_in_mongo(profileid, datasetobj):
    dataset = json.dumps(datasetobj, default=lambda x: x.__dict__)
    dataset = json.loads(dataset)
    id = ObjectId(profileid)
    result = db.collection.update_one({'_id':id}, {"$set": dataset}, upsert=False)

    return result.acknowledged, dataset

"""
create FileDescriptor object
"""
def create_file_descriptor(data_repo_dir, file):
    filename = file.filename
    fd = FileDescriptor()
    new_id = ObjectId()
    new_id = str(new_id)
    fd.set_id(new_id)

    # create folder
    levels = 2
    path = ''
    i = 0
    while (i < levels * 2 and len(new_id) >= i + 2):
        path = path + new_id[i: i + 2] + os.sep
        i = i + 2

    if (len(new_id) > 0):
        path = path + new_id + os.sep

    path = data_repo_dir + os.sep + path

    if not os.path.exists(path):
        os.makedirs(path)

    # save file to path
    file.save(os.path.join(path, filename))

    # if os.path.isfile(filename):
    #     shutil.copy(filename, path)

    saved_file = path + os.path.basename(filename)
    fd.set_data_url('file:' + os.sep + saved_file)

    fd.set_filename(os.path.basename(filename))

    mime = MimeTypes()
    mime_type = mime.guess_type(urllib.request.pathname2url(filename))
    if mime_type[0] == None:
        fd.set_mime_type('application/octet-stream')
    else:
        fd.set_mime_type(mime_type[0])

    file_stat = os.stat(saved_file)
    fd.set_size(file_stat.st_size)

    hash_md5 = hashlib.md5()
    with open(saved_file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    fd.set_md5sum(hash_md5.hexdigest())

    return fd


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
