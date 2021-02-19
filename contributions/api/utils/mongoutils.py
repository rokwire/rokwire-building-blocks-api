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

client_contribution = MongoClient(cfg.MONGO_CONTRIBUTION_URL, connect=False)
db_contribution = client_contribution[cfg.CONTRIBUTION_DB_NAME]
coll_contribution = db_contribution[cfg.CONTRIBUTION_COLL_NAME]
# coll_contribution.create_index([("name", ASCENDING)], background=True)
# coll_contribution.create_index([("capabilities.name", ASCENDING)], background=True)
# coll_contribution.create_index([("talents.name", ASCENDING)], background=True)
# This has to be done for applying the following index being applied
if len(coll_contribution.index_information()) > 3:
    coll_contribution.drop_index('*')
coll_contribution.create_index([("name" , TEXT),("capabilities.name", TEXT),("talents.name", TEXT)],name="name_index")


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
        db_data = db_collection.find({}, {'_id': 0})
    else:
        db_data = db_collection.find(query, {'_id': 0})

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

def get_result_text_meta_score(db_collection, search_field, search_word):
    db_data = db_collection.find({'$text': {'$search': search_word}},
                                 {'score': {'$meta': 'textScore'}})
    db_data.sort([('score', {'$meta': 'textScore'})])
    data_list = list(db_data)

    # remove object id
    for data in data_list:
        del (data['_id'])
        del (data['score'])

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
def get_contribution_dataset_from_field(collection, fld, query_str):
    db_data = query_dataset(collection, fld, query_str)
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
def get_contribution_dataset_from_objectid(collection, objectid):
    is_object_id = check_if_objectid(objectid)
    if is_object_id:
        id = ObjectId(objectid)
        db_data = query_dataset_by_objectid(collection, id)
        data_list = list(db_data)
        if len(data_list) > 0:
            data_dump = dumps(data_list)
            data_dump = data_dump[:-1]
            data_dump = data_dump[1:]
            json_load = json.loads(data_dump)
            dataset = Contribution(json_load)

            return dataset
        else:
            return None
    else:
        return None

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
def query_dataset_by_objectid(collection, objectid):
    return collection.find({'_id': objectid})

"""
qyery dataset using field
"""
def query_dataset(db_collection, fld, query_str):
    return db_collection.find({fld: query_str}, {'_id': False})

"""
construct json from mongo query
"""
def construct_json_from_query_list(data_list):
    data_dump = dumps(data_list)
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
index capability collection
"""
def index_capability_data(collection):
    collection.create_index([('name', ASCENDING), ('version', ASCENDING), ('description', ASCENDING)])
