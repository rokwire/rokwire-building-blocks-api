import json
import logging
import controllers.configs as cfg

from bson import ObjectId
from flask import make_response, json
from bson.json_util import dumps
from pymongo import MongoClient, ASCENDING

from models.capabilities.capability import Capability
import utils.jsonutils as jsonutils

client_contribution = MongoClient(cfg.MONGO_CONTRIBUTION_URL, connect=False)
db_contribution = client_contribution[cfg.CONTRIBUTION_DB_NAME]
db_contribution.contribution_collection = db_contribution[cfg.CONTRIBUTION_COLL_NAME]
db_contribution.capability_collection = db_contribution[cfg.CAPABILITY_COLL_NAME]

"""
get query output json of capability from query using search arguments
"""
def get_result(db_collection, query):
    if not query:
        return None

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

"""
get query output json from field name and query string
"""
def get_capability_http_output_query_result_using_field_string(fld, query_str):
    outjson = get_capability_query_json_from_field(fld, query_str)
    if (outjson is not None) and (len(outjson)) > 0:
        data_dump = dumps(outjson)
        out_json = make_response(data_dump)
        out_json.mimetype = 'application/json'

        msg = "request capability information: " + str(query_str)
        logging.debug(msg)

        return out_json
    else:
        msg = "the dataset does not exist with name of : " + str(query_str)
        logging.error(msg)

        return None

"""
query capability using field name and querystring and convert result to capability object
"""
def get_dataset_from_field(db_collection, fld, query_str):
    db_data = query_dataset(db_collection, fld, query_str)
    data_list = list(db_data)
    if len(data_list) == 1:
        data_dump = dumps(data_list)
        data_dump = data_dump[:-1]
        data_dump = data_dump[1:]
        json_load = json.loads(data_dump)
        dataset = Capability(json_load)

        try:
            dataset.set_name(json_load[cfg.FIELD_NAME])
        except:
            pass

        return dataset

    elif len(data_list) > 1:
        #TODO create a method to handle this

        return None

    else:
        msg = 'there is no output query result or multiple query result'
        logging.debug(msg)

        return None

"""
query capability using objectid and convert result to capability object
"""
def get_capability_dataset_from_objectid(objectid):
    is_capability_id = check_if_objectid(objectid)
    if is_capability_id:
        id = ObjectId(objectid)
        db_data = query_capability_dataset_by_objectid(id)
        data_list = list(db_data)
        if len(data_list) > 0:
            data_dump = dumps(data_list)
            data_dump = data_dump[:-1]
            data_dump = data_dump[1:]
            json_load = json.loads(data_dump)
            dataset = Capability(json_load)

            return dataset
        else:
            return None
    else:
        return None

"""
convert capability mongodb query using field result to json
"""
def get_capability_query_json_from_field(fld, query_str):
    db_data = query_dataset(db_collection, fld, query_str)
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
query capability dataset using object id
"""
def query_capability_dataset_by_objectid(objectid):
    return db_contribution.capability_collection.find({'_id': objectid})

"""
qyery capability dataset using field
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
insert capability dataset to mognodb
"""
def insert_dataset_to_mongodb(db_collection, indataset):
    dataset = json.dumps(indataset, default=lambda x: x.__dict__)
    dataset = json.loads(dataset)

    id = db_collection.insert(dataset)

    return dataset, id

"""
update capability dataset in mongodb by objectid
"""
def update_capability_dataset_in_mongo_by_objectid(objectid, datasetobj):
    dataset = json.dumps(datasetobj, default=lambda x: x.__dict__)
    dataset = json.loads(dataset)
    id = ObjectId(objectid)
    result = db_contribution.capability_collection.update_one({'_id': id}, {"$set": dataset}, upsert=False)

    return result.acknowledged, dataset

"""
update capability dataset in mongodb by field
"""
def update_capability_dataset_in_mongo_by_field(fld, query_str, datasetobj):
    dataset = json.dumps(datasetobj, default=lambda x: x.__dict__)
    dataset = json.loads(dataset)
    result = db_contribution.capability_collection.update_one({fld: query_str}, {"$set": dataset}, upsert=False)

    return result.acknowledged, dataset

"""
update json that doesn't belong to data schema
"""
def update_json_with_no_schema(fld, query_str, datasetobj, restjson):
    dataset = db_contribution.capability_collection.find({fld: query_str}, {'_id': False})
    dataset = json.dumps(datasetobj, default=lambda x: x.__dict__)
    dataset = json.loads(dataset)
    for dictkey, dictelement in restjson.items():
        tmpDict = {dictkey: dictelement}
        dataset.update(tmpDict)
        result = db_contribution.capability_collection.update_one({fld: query_str}, {"$set": tmpDict}, upsert=False)

    return result.acknowledged, dataset

"""
index capability collection
"""
def index_capability_data():
    db_contribution.capability_collection.create_index([('name', ASCENDING),
                                                        ('version', ASCENDING),
                                                        ('description', ASCENDING)])