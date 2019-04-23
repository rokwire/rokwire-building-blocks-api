"""
author: Yong Wook Kim (NCSA ywkim@illinois.edu)
created 2019 Apr 22
"""
import json
import logging
import profileservice.configs as cfg

from bson import ObjectId
from bson.json_util import dumps
from flask import make_response
from pymongo import MongoClient

from profileservice.dao.profiledataset import ProfileDataset

client = MongoClient(cfg.PROFILE_MONGO_URL, connect=False)
db = client[cfg.PROFILE_DB_NAME]
db.collection = db[cfg.PROFILE_DB_COLL_NAME]

"""
get query output json from field name and query string
"""
def get_http_output_query_result_using_field_string(fld, query_str):
    outjson = get_query_json_from_field(fld, query_str)
    if (outjson is not None) and (len(outjson)) > 0:
        data_dump = dumps(outjson)
        out_json = make_response(data_dump)
        out_json.mimetype = 'application/json'

        msg = "request profile information: " + str(query_str)
        logging.debug(msg)

        return out_json
    else:
        msg = "the dataset does not exist with uuid of : " + str(query_str)
        logging.error(msg)

        return None

"""
convert mongodb query result to profile object using object id
"""
def get_dataset_from_objectid(objectid):
    is_profile_id = check_if_objectid(objectid)
    if is_profile_id:
        id = ObjectId(objectid)
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
convert mongodb query result to profile object using query field
"""
def get_query_dataset_from_field(fld, query_str):
    db_data = query_dataset(fld, query_str)
    data_list = list(db_data)
    if len(data_list) == 1:
        json_load = get_query_json_from_field(fld, query_str)
        if json_load != None:
            dataset = ProfileDataset(json_load)
        else:
            return None

        return dataset
    else:
        msg = 'there is no output query result or multiple query result'
        logging.debug(msg)

        return None

"""
convert mongodb query result to json
"""
def get_query_json_from_field(fld, query_str):
    db_data = query_dataset(fld, query_str)
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
def query_dataset_by_objectid(objectid):
    return db.collection.find({'_id': objectid})

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
update profile dataset in mongodb by objectid
"""
def update_dataset_in_mongo_by_objectid(objectid, datasetobj):
    dataset = json.dumps(datasetobj, default=lambda x: x.__dict__)
    dataset = json.loads(dataset)
    id = ObjectId(objectid)
    result = db.collection.update_one({'_id': id}, {"$set": dataset}, upsert=False)

    return result.acknowledged, dataset

"""
update profile dataset in mongodb by field
"""
def update_dataset_in_mongo_by_field(fld, query_str, datasetobj):
    dataset = json.dumps(datasetobj, default=lambda x: x.__dict__)
    dataset = json.loads(dataset)
    result = db.collection.update_one({fld: query_str}, {"$set": dataset}, upsert=False)

    return result.acknowledged, dataset