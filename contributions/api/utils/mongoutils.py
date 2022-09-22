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

import json
import logging
import controllers.configs as cfg

from bson import ObjectId
from flask import make_response, json
from bson.json_util import dumps
from pymongo import MongoClient, ASCENDING, TEXT
from models.contribution import Contribution
from utils import query_params
from utils import jsonutils
from utils import adminutils

client_contribution = MongoClient(cfg.MONGO_CONTRIBUTION_URL, connect=False)
db_contribution = client_contribution[cfg.CONTRIBUTION_DB_NAME]
coll_contribution = db_contribution[cfg.CONTRIBUTION_COLL_NAME]  # set contribution collection
# create compound text indexes with equal weightage
coll_contribution.create_index([("name", TEXT), ("capabilities.name", TEXT), ("talents.name", TEXT)], default_language='english')

coll_reviewer = db_contribution[cfg.REVIEWER_COLL_NAME]  # set reviewer collection
coll_reviewer.create_index([("name", TEXT)])

"""
get json of all the contributions list
"""
def list_contributions(db_collection):
    db_data = db_collection.find({}, {'_id': False})
    data_list = list(db_data)

    if len(data_list) > 0:
        data_dump = dumps(data_list)
        if len(data_list) == 1: # remove blacket in the first and last character location
            data_dump = data_dump[:-1]
            data_dump = data_dump[1:]
        json_load = json.loads(data_dump)

        return json_load
    else:
        return None

"""
get json of all the talent list
"""
def list_talents(db_collection):
    db_data = db_collection.find({}, {'talents':1, '_id':0})
    data_list = list(db_data)

    if len(data_list) > 0:
        data_dump = dumps(data_list)
        if len(data_list) == 1: # remove blacket in the first and last character location
            data_dump = data_dump[:-1]
            data_dump = data_dump[1:]
        json_load = json.loads(data_dump)

        return json_load
    else:
        return None

"""
get json of all the capabilities list
"""
def list_capabilities(db_collection):
    db_data = db_collection.find({}, {'capabilities':1, '_id':0})
    data_list = list(db_data)

    if len(data_list) > 0:
        data_dump = dumps(data_list)
        if len(data_list) == 1: # remove blacket in the first and last character location
            data_dump = data_dump[:-1]
            data_dump = data_dump[1:]
        json_load = json.loads(data_dump)

        return json_load
    else:
        return None

def get_result(db_collection, query):
    if not query:
        # db_data = db_collection.find({}, {'_id': 0})
        db_data = db_collection.find({})
    else:
        # db_data = db_collection.find(query, {'_id': 0})
        db_data = db_collection.find(query)

    data_list = list(db_data)
    print(data_list)

    if len(data_list) > 0:
        data_dump = dumps(data_list)
        json_load = json.loads(data_dump)
        json_load = jsonutils.convert_obejctid_from_dataset_json_list(json_load)

        return json_load
    else:
        return None

"""
get query output json from field name and query string
"""
def get_http_output_query_result_using_field_string(collection, fld, query_str):
    outjson = get_query_json_from_field(collection, fld, query_str)
    if (outjson is not None) and (len(outjson)) > 0:
        data_dump = dumps(outjson)
        out_json = make_response(data_dump)
        out_json.mimetype = 'application/json'

        msg = "request information: " + str(query_str)
        logging.debug(msg)

        return out_json
    else:
        msg = "the dataset does not exist with name of : " + str(query_str)
        logging.error(msg)

        return None

"""
query using field name and querystring and convert result to object
"""
def get_contribution_dataset_from_field_no_status(collection, fld, query_str):
    db_data = query_dataset_no_status(collection, fld, query_str)
    data_list = list(db_data)
    if len(data_list) == 1:
        data_dump = dumps(data_list)
        data_dump = data_dump[:-1]
        data_dump = data_dump[1:]
        json_load = json.loads(data_dump)
        dataset = Contribution(json_load)

        try:
            dataset.set_name(json_load[cfg.FIELD_NAME])
        except:
            pass

        return dataset

    elif len(data_list) > 1:
        #TODO create a method to handle this

        return data_list

    else:
        msg = 'there is no output query result or multiple query result'
        logging.debug(msg)

        return None

"""
query using objectid and convert result to object
"""
def get_contribution_dataset_from_objectid_no_status(collection, objectid):
    is_object_id = check_if_objectid(objectid)
    if is_object_id:
        id = ObjectId(objectid)
        db_data = query_dataset_by_objectid_no_status(collection, id)
        data_list = list(db_data)
        if len(data_list) == 1:
            data_dump = dumps(data_list)
            data_dump = data_dump[:-1]
            data_dump = data_dump[1:]
            json_load = json.loads(data_dump)
            json_load = jsonutils.convert_obejctid_from_dataset_json(json_load)
            dataset = Contribution(json_load)

            return dataset
        else:
            return None
    else:
        return None

"""
query using objectid and convert result to object
"""
def get_contribution_dataset_from_objectid(collection, objectid, login_id=None, is_login=False):
    is_object_id = check_if_objectid(objectid)
    status_code = '200'

    if is_object_id:
        id = ObjectId(objectid)
        # check the data first without status, if there is no result, it is 404
        db_data = query_dataset_by_objectid_no_status(collection, id)
        data_list = list(db_data)

        # no result is only 404
        if len(data_list) == 0:
            status_code = '404'
            return None, status_code

        # multiple result is only 400
        if len(data_list) > 1:
            status_code = '400'
            return None, status_code

        # check the data status, if the status is not published, it is 401
        tmp_dataset = data_list[0]
        status = None
        is_admin = False
        if "status" in tmp_dataset:
            status = tmp_dataset["status"]
        if (is_login):
            if "contributionAdmins" in tmp_dataset:
                contribution_admins = tmp_dataset["contributionAdmins"]
                if (login_id in contribution_admins):
                    is_admin = True

        data_dump = dumps(data_list)
        data_dump = data_dump[:-1]
        data_dump = data_dump[1:]
        json_load = json.loads(data_dump)
        json_load = jsonutils.convert_obejctid_from_dataset_json(json_load)
        dataset = Contribution(json_load)

        if status == "Published":
            return dataset, status_code
        else:
            if is_login:
                # check if the user is in contributionAdmin group
                if is_admin:
                    return dataset, status_code
                else:
                    status_code = '401'
                    return None, status_code
            else:
                # if not logged in and if status is not Published return unauthorized
                status_code = '401'
                return None, status_code

    else:
        status_code = '400'
        return None, status_code

"""
convert mongodb query using field result to json
"""
def get_query_json_from_field(collection, fld, query_str):
    db_data = query_dataset(collection, fld, query_str)
    data_list = list(db_data)
    if len(data_list) > 0:
        data_dump = dumps(data_list)
        data_dump = data_dump[:-1]
        data_dump = data_dump[1:]
        json_load = json.loads(data_dump)
        json_load = jsonutils.convert_obejctid_from_dataset_json_list(json_load)

        return json_load
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
def query_dataset_by_objectid(collection, objectid, login_id=None, is_login=False):
    query = dict()
    query = query_params.format_query_status_login(query, login_id, is_login)

    query_parts = [{'_id': objectid}]
    query['$and'] = query_parts

    return collection.find(query)

"""
query dataset using object id
"""
def query_dataset_by_objectid_no_status(collection, objectid):
    return collection.find({'_id': objectid})

"""
qyery dataset using field
"""
def query_dataset(db_collection, fld, query_str, login_id=None, is_login=False):
    query = dict()
    query = query_params.format_query_status_login(query, login_id, is_login)

    query_parts = [{fld: query_str}]
    query['$and'] = query_parts
    return db_collection.find(query)

"""
qyery dataset using field
"""
def query_dataset_no_status(db_collection, fld, query_str):
    return db_collection.find({fld: query_str})

"""
construct json from mongo query
"""
def construct_json_from_query_list(in_json, login_id=None):
    # check if the user is a reviewer or admin, otherwise, remove review from the output
    if login_id is not None:
        is_reviewer = adminutils.check_if_reviewer(login_id)
        # remove review if the requested user is not reviewer
        if not is_reviewer:
            if "review" in in_json:
                del in_json["review"]
    data_dump = dumps(in_json)
    out_json = make_response(data_dump)
    out_json.mimetype = 'application/json'

    return out_json

"""
insert dataset to mognodb
"""
def insert_dataset_to_mongodb(db_collection, indataset):
    dataset = json.dumps(indataset, default=lambda x: x.__dict__)
    dataset = json.loads(dataset)

    id = db_collection.insert(dataset)

    return dataset, id

"""
update dataset in mongodb by objectid
"""
def update_dataset_in_mongo_by_objectid(collection, objectid, datasetobj):
    dataset = json.dumps(datasetobj, default=lambda x: x.__dict__)
    dataset = json.loads(dataset)
    id = ObjectId(objectid)
    result = collection.update_one({'_id': id}, {"$set": dataset}, upsert=False)

    return result.acknowledged, dataset

"""
update dataset in mongodb by field
"""
def update_dataset_in_mongo_by_field(collection, fld, query_str, datasetobj):
    dataset = json.dumps(datasetobj, default=lambda x: x.__dict__)
    dataset = json.loads(dataset)
    result = collection.update_one({fld: query_str}, {"$set": dataset}, upsert=False)

    return result.acknowledged, dataset

"""
update json that doesn't belong to data schema
"""
def update_json_with_no_schema(collection, fld, query_str, datasetobj, restjson):
    dataset = collection.find({fld: query_str}, {'_id': False})
    dataset = json.dumps(datasetobj, default=lambda x: x.__dict__)
    dataset = json.loads(dataset)
    for dictkey, dictelement in restjson.items():
        tmpDict = {dictkey: dictelement}
        dataset.update(tmpDict)
        result = collection.update_one({fld: query_str}, {"$set": tmpDict}, upsert=False)

    return result.acknowledged, dataset

"""
get json of all the reviewers list
"""
def list_reviewers():
    db_data = coll_reviewer.find({})
    data_list = list(db_data)

    if len(data_list) > 0:
        data_dump = dumps(data_list)
        json_load = json.loads(data_dump)
        json_load = jsonutils.convert_obejctid_from_dataset_json_list(json_load)

        return json_load
    else:
        return None

def get_reviewers_record(username):
    """
    Method to return the record of a reviewer from mongodb reviewer collection
    Args:
        username (str): github username
    Returns:
        (json) : json output from mongodb find query
    """
    db_data = coll_reviewer.find({"githubUsername": username})
    data_list = list(db_data)

    if len(data_list) > 0:
        data_dump = dumps(data_list)
        json_load = json.loads(data_dump)
        json_load = jsonutils.convert_obejctid_from_dataset_json_list(json_load)
        return json_load
    else:
        return None


"""
query using query field and querystring and convert result to object
"""
def get_dataset_from_field(collection, fld, query_str):
    db_data = query_dataset_no_status(collection, fld, query_str)
    data_list = list(db_data)
    if len(data_list) == 1:
        data_dump = dumps(data_list)
        data_dump = data_dump[:-1]
        data_dump = data_dump[1:]
        json_load = json.loads(data_dump)
        dataset = Contribution(json_load)

        try:
            dataset.set_name(json_load[cfg.FIELD_NAME])
        except:
            pass

        return dataset

    elif len(data_list) > 1:
        #TODO create a method to handle this

        return data_list

    else:
        msg = 'there is no output query result or multiple query result'
        logging.debug(msg)

        return None

"""
index capability collection
"""
def index_capability_data(collection):
    collection.create_index([('name', ASCENDING), ('version', ASCENDING), ('description', ASCENDING)])
