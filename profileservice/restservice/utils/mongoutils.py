import json
import logging
import profileservice.configs as cfg


from bson import ObjectId
from bson.json_util import dumps
from flask import make_response
from pymongo import MongoClient

from profileservice.dao.non_pii_data import non_pii_data
from profileservice.dao.pii_data import pii_data
import profileservice.restservice.utils.jsonutils as jsonutils

client_profile = MongoClient(cfg.MONGO_PROFILE_URL, connect=False)
db_profile = client_profile[cfg.PROFILE_DB_NAME]
db_profile.non_pii_collection = db_profile[cfg.PROFILE_DB_PROFILE_COLL_NAME]
client_pii = MongoClient(cfg.MONGO_PII_URL, connect=False)
db_pii = client_pii[cfg.PII_DB_NAME]
db_pii.pii_collection = db_pii[cfg.PII_DB_PII_COLL_NAME]

"""
get query output json from field name and query string
"""
def get_pii_http_output_query_result_using_field_string(fld, query_str):
    outjson = get_pii_query_json_from_field(fld, query_str)
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
query non-pii using objectid and convert result to non-pii object
"""
def get_non_pii_dataset_from_objectid(objectid):
    is_profile_id = check_if_objectid(objectid)
    if is_profile_id:
        id = ObjectId(objectid)
        db_data = query_non_pii_dataset_by_objectid(id)
        data_list = list(db_data)
        if len(data_list) > 0:
            data_dump = dumps(data_list)
            data_dump = data_dump[:-1]
            data_dump = data_dump[1:]
            json_load = json.loads(data_dump)
            dataset = non_pii_data(json_load)

            return dataset
        else:
            return None
    else:
        return None

"""
query non-pii using field name and querystring and convert result to non-pii object
"""
def get_non_pii_dataset_from_field(fld, query_str):
    db_data = query_non_pii_dataset(fld, query_str)
    data_list = list(db_data)
    if len(data_list) == 1:
        data_dump = dumps(data_list)
        data_dump = data_dump[:-1]
        data_dump = data_dump[1:]
        json_load = json.loads(data_dump)
        dataset = non_pii_data(json_load)

        try:
            dataset.set_uuid(json_load[cfg.FIELD_PROFILE_UUID])
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
query pii using field name and querystring and convert result to non-pii object
"""
def get_pii_dataset_from_field(fld, query_str):
    db_data = query_pii_dataset(fld, query_str)
    data_list = list(db_data)
    if len(data_list) == 1:
        data_dump = dumps(data_list)
        data_dump = data_dump[:-1]
        data_dump = data_dump[1:]
        json_load = json.loads(data_dump)
        dataset = pii_data(json_load)

        try:
            dataset.set_uuid(json_load[cfg.FIELD_PROFILE_UUID])
        except:
            pass
        try:
            dataset.set_pid(json_load[cfg.FIELD_PID])
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
convert non-pii mongodb query using field result to json
"""
def get_non_pii_query_json_from_field(fld, query_str):
    db_data = query_non_pii_dataset(fld, query_str)
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
convert pii mongodb query using field result to json
"""
def get_pii_query_json_from_field(fld, query_str):
    db_data = query_pii_dataset(fld, query_str)
    data_list = list(db_data)

    # remove fileDescriptors from db_data
    data_list = jsonutils.remove_file_descriptor_from_data_list(data_list)

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
query non pii dataset using object id
"""
def query_non_pii_dataset_by_objectid(objectid):
    return db_profile.non_pii_collection.find({'_id': objectid})

"""
qyery non pii dataset using field
"""
def query_non_pii_dataset(fld, query_str):
    return db_profile.non_pii_collection.find({fld: query_str}, {'_id': False})

"""
qyery pii dataset using field
"""
def query_pii_dataset(fld, query_str):
    return db_pii.pii_collection.find({fld: query_str}, {'_id': False})

"""
construct json from mongo query
"""
def construct_json_from_query_list(data_list):
    data_dump = dumps(data_list)
    out_json = make_response(data_dump)
    out_json.mimetype = 'application/json'

    return out_json

"""
insert non pii dataset to mognodb
"""
def insert_non_pii_dataset_to_mongodb(indataset):
    dataset = json.dumps(indataset, default=lambda x: x.__dict__)
    dataset = json.loads(dataset)

    id = db_profile.non_pii_collection.insert(dataset)

    return dataset, id

"""
insert pii dataset to mognodb
"""
def insert_pii_dataset_to_mongodb(indataset):
    dataset = json.dumps(indataset, default=lambda x: x.__dict__)
    dataset = json.loads(dataset)

    id = db_pii.pii_collection.insert(dataset)

    return dataset

"""
update non pii dataset in mongodb by objectid
"""
def update_non_pii_dataset_in_mongo_by_objectid(objectid, datasetobj):
    dataset = json.dumps(datasetobj, default=lambda x: x.__dict__)
    dataset = json.loads(dataset)
    id = ObjectId(objectid)
    result = db_profile.non_pii_collection.update_one({'_id': id}, {"$set": dataset}, upsert=False)

    return result.acknowledged, dataset

"""
update non pii dataset in mongodb by field
"""
def update_non_pii_dataset_in_mongo_by_field(fld, query_str, datasetobj):
    dataset = json.dumps(datasetobj, default=lambda x: x.__dict__)
    dataset = json.loads(dataset)
    result = db_profile.non_pii_collection.update_one({fld: query_str}, {"$set": dataset}, upsert=False)

    return result.acknowledged, dataset

"""
update pii dataset in mongodb by objectid
"""
def update_pii_dataset_in_mongo_by_objectid(objectid, datasetobj):
    dataset = json.dumps(datasetobj, default=lambda x: x.__dict__)
    dataset = json.loads(dataset)
    id = ObjectId(objectid)
    result = db_pii.pii_collection.update_one({'_id': id}, {"$set": dataset}, upsert=False)

    return result.acknowledged, dataset

"""
update pii dataset in mongodb by field
"""
def update_pii_dataset_in_mongo_by_field(fld, query_str, datasetobj):
    dataset = json.dumps(datasetobj, default=lambda x: x.__dict__)
    dataset = json.loads(dataset)
    result = db_pii.pii_collection.update_one({fld: query_str}, {"$set": dataset}, upsert=False)

    return result.acknowledged, dataset

"""
index non pii collection
"""
def index_non_pii_data():
    db_profile.non_pii_collection.create_index([('uuid', 'text'),
                            ('generalInterests', 'text'),
                            ('athleticsInterests', 'text')])

"""
index non pii collection
"""
def index_pii_data():
    db_pii.pii_collection.create_index([('pid', 'text'),
                             ('firstname', 'text'),
                             ('lastname', 'text'),
                             ('email', 'text'),
                             ('username', 'text'),
                             ('uin', 'text'), ('netid', 'text'),
                             ('phone', 'text')])