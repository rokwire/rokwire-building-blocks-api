"""
author: Yong Wook Kim
created 2019 Apr 5
"""
#!flask/bin/python
import pymongo
import logging
import flask
import os
import json

from bson import ObjectId
from flask import jsonify
from pymongo import MongoClient
from flask import make_response
from profileservice.dao.profiledataset import ProfileDataset

from flask import request
from bson.json_util import dumps


app = flask.Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

mongo_url = os.getenv('MONGODB_URI', 'localhost:27017')
db_name = os.getenv('DB_NAME', 'profiledb')
coll_name = os.getenv('DB_COLLECTION', 'ProfileDataset')

client = pymongo.MongoClient(mongo_url, connect=False)
db = client[db_name]
db.collection = db[coll_name]
__logger = logging.getLogger("rokwire-building-blocks-api")


"""
rest service for root directory
"""
@app.route('/profiles', methods = ['GET', 'POST'])
def root_dir():
    if request.method == 'GET':
        db_data = db.collection.find({}, {'_id': False})
        data_list = list(db_data)
        data_dump = dumps(data_list)
        out_json = make_response(data_dump)
        out_json.mimetype = 'application/json'
        logging.debug("list all profiles")

        return out_json

    if request.method == 'POST':
        in_json = request.get_json()
        profile = ProfileDataset(in_json)
        dataset, id = insert_profile_to_mongodb(mongo_url, profile)

        data_dump = dumps(dataset)
        out_json = make_response(data_dump)
        out_json.mimetype = 'application/json'
        logging.debug("list all profiles")

        msg = "data has been posted: " + str(id)
        logging.debug(msg)

        return out_json

"""
provide profile information by profile id or remove it
"""
@app.route('/profiles/<profileid>', methods = ['GET', 'DELETE'])
def deal_profile_id(profileid):
    out_json = None
    is_profile_id = True

    if profileid != None:
        # check if the input variable is either object id or user name
        try:
            id = ObjectId(profileid)
        except:
            is_profile_id = False

        # query using either profile id or user name
        if (is_profile_id):
            id = ObjectId(profileid)
            db_data = db.collection.find({'_id':id})
        else:
            db_data = db.collection.find({'username': profileid})

        # construct output json
        data_list = list(db_data)
        if len(data_list) > 0:
            data_dump = dumps(data_list)
            out_json = make_response(data_dump)
            out_json.mimetype = 'application/json'

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
                    return not_found()

            return out_json
        else:
            return not_found()


"""
insert profile json to mognodb
"""
def insert_profile_to_mongodb(mongo_url, indataset):
    client = MongoClient(mongo_url, 27017)
    db = client['profiledb']
    coll = db.ProfileDataset

    dataset = json.dumps(indataset, default=lambda x: x.__dict__)
    dataset = json.loads(dataset)

    id = coll.insert(dataset)

    return dataset, id

@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
