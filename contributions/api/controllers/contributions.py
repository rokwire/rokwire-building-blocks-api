import json
import datetime
import logging
import copy

from flask import jsonify, request, g
from bson import ObjectId

import controllers.configs as cfg
import utils.jsonutils as jsonutils
import utils.datasetutils as datasetutils
import utils.rest_handlers as rs_handlers
import utils.otherutils as otherutils
import utils.tokenutils as tokenutils
import utils.mongoutils as mongoutils

from utils import query_params
from models.contribution import Contribution
from models.person import Person
from models.organization import Organization
from models.capabilities.capability import Capability
from pymongo import MongoClient, ASCENDING

client_contribution = MongoClient(cfg.MONGO_CONTRIBUTION_URL, connect=False)
db_contribution = client_contribution[cfg.CONTRIBUTION_DB_NAME]
coll_contribution = db_contribution[cfg.CONTRIBUTION_COLL_NAME]

def post():
    is_new_install = True

    # check if name is in there otherwise it is either a first installation
    try:
        in_json = request.get_json()
        name = in_json[cfg.FIELD_NAME]
        # check if the dataset is existing with given name
        dataset = mongoutils.get_contribution_dataset_from_field(coll_contribution, cfg.FIELD_NAME, name)
        if dataset is not None:
            is_new_install = False
            msg = {
                "reason": "NAME in input json already exists in the database: " + str(name),
                "error": "Bad Request: " + request.url,
            }
            msg_json = jsonutils.create_log_json("Contribution", "POST", msg)
            logging.error("POST " + json.dumps(msg_json))
            return rs_handlers.bad_request(msg)
    except:
        pass

    if is_new_install:
        # new installation of the app
        currenttime = datetime.datetime.now()
        currenttime = currenttime.strftime("%Y/%m/%dT%H:%M:%S")
        contribution_dataset = Contribution('')
        contribution_dataset, restjson = datasetutils.update_capability_dataset_from_json(contribution_dataset, in_json)
        contribution_dataset.set_date_created(currenttime)
        contribution_dataset.set_date_modified(currenttime)

        # set contributors list
        contributors_list = []
        try:
            contributors_json = in_json["contributors"]
            for i in range(len(contributors_json)):
                contributor, rest_contributor_json, msg = construct_contributors(contributors_json[i])
                if contributor is None:
                    return rs_handlers.bad_request(msg)
                contributors_list.append(contributor)
            contribution_dataset.set_contributors(contributors_list)
        except:
            pass

        # set capability list
        capability_list = []
        try:
            capability_json = in_json["capabilities"]
            for i in range(len(capability_json)):
                capability, rest_capability_json, msg = construct_capability(capability_json[i])
                if capability is None:
                    return rs_handlers.bad_request(msg)
                capability_list.append(capability)
            contribution_dataset.set_capabilities(capability_list)
        except:
            pass

        # insert contribution dataset
        dataset, id = mongoutils.insert_dataset_to_mongodb(coll_contribution, contribution_dataset)
        contribution_name = dataset[cfg.FIELD_NAME]
        contribution_id = str(dataset['_id'])

        # use this if it needs to return actual dataset
        dataset = jsonutils.remove_objectid_from_dataset(dataset)
        # out_json = mongoutils.construct_json_from_query_list(dataset)
        msg = "new contribution has been created: " + str(contribution_name)
        msg_json = jsonutils.create_log_json("Contribution", "POST", dataset)
        logging.info("POST " + json.dumps(msg_json))

        return rs_handlers.return_id(msg, 'id', contribution_id)

def search():
    args = request.args
    query = dict()
    try:
        query = query_params.format_query_contribution(args, query)
    except Exception as ex:
        msg = {
            "reason": "The query is wrong or bad argument " + str(args),
            "error": "Bad Request: " + request.url,
        }
        msg_json = jsonutils.create_log_json("Contribution", "SEARCH", msg)
        logging.error("Contribution SEARCH " + json.dumps(msg_json))
        return rs_handlers.bad_request(msg_json)

    try:
        out_json = mongoutils.get_result(coll_contribution, query)
    except Exception as ex:
        msg = {
            "reason": "The query is wrong or bad argument " + str(args),
            "error": "Bad Request: " + request.url,
        }
        msg_json = jsonutils.create_log_json("Contribution", "SEARCH", msg)
        logging.error("Contribution SEARCH " + json.dumps(msg_json))
        return rs_handlers.bad_request(msg_json)

    if out_json is None:
        out_json = []

    msg = {
        "search": "Contribution search performed with arguments of : " + str(args),
        "result": out_json,
    }
    msg_json = jsonutils.create_log_json("Contribution", "SEARCH", msg)
    logging.info("Contribution SEARCH " + json.dumps(msg))

    return out_json

def get(id=None):
    data_list, is_objectid, is_error, resp = get_data_list(id)
    if is_error:
        return resp
    jsonutils.remove_objectid_from_dataset(data_list[0])
    out_json = mongoutils.construct_json_from_query_list(data_list[0])
    msg_json = jsonutils.create_log_json("Contribution", "GET", data_list[0])
    logging.info("Contribution GET " + json.dumps(jsonutils.remove_objectid_from_dataset(msg_json)))

    return out_json

def put(id=None):
    try:
        in_json = request.get_json()
    except Exception as ex:
        msg = {
            "reason": "Json format error: " + str(id),
            "error": "Bad Request: " + request.url,
        }
        msg_json = jsonutils.create_log_json("Contribution", "PUT", msg)
        logging.error("PUT " + json.dumps(msg_json))
        return rs_handlers.bad_request(msg_json)
    # check if the given id exists
    contribution_dataset = mongoutils.get_contribution_dataset_from_objectid(coll_contribution, id)
    date_created = contribution_dataset.dateCreated

    if contribution_dataset is None:
        msg = {
            "reason": "There is no contribution dataset with given id: " + str(id),
            "error": "Not Found: " + request.url,
        }
        msg_json = jsonutils.create_log_json("Contribution", "PUT", msg)
        logging.error("PUT " + json.dumps(msg_json))
        return rs_handlers.not_found(msg_json)


    contribution_dataset, restjson = datasetutils.update_contribution_dataset_from_json(contribution_dataset, in_json)
    currenttime = datetime.datetime.now()
    currenttime = currenttime.strftime("%Y/%m/%dT%H:%M:%S")
    contribution_dataset.set_date_modified(currenttime)
    contribution_dataset.set_date_created(date_created)

    # set capability list
    capability_list = []
    try:
        capability_json = in_json["capabilities"]
        for i in range(len(capability_json)):
            capability, rest_capability_json, msg = construct_capability(capability_json[i])
            if capability is None:
                return rs_handlers.bad_request(msg)
            capability_list.append(capability)
        contribution_dataset.set_capabilities(capability_list)
    except:
        pass

    result, contribution_dataset = mongoutils.update_dataset_in_mongo_by_objectid(coll_contribution, id, contribution_dataset)

    if result is None:
        msg = {
            "reason": "Failed to update contribution dataset: " + str(id),
            "error": "Not Implemented: " + request.url,
        }
        msg_json = jsonutils.create_log_json("Contribution", "PUT", msg)
        logging.error("PUT " + json.dumps(msg_json))
        return rs_handlers.not_implemented(msg_json)

    # capability_dataset = jsonutils.remove_file_descriptor_from_dataset(capability_dataset)
    # out_json = jsonutils.remove_null_subcategory(capability_dataset)
    out_json = contribution_dataset
    msg_json = jsonutils.create_log_json("Contribution", "PUT", copy.copy(out_json))
    logging.info("PUT " + json.dumps(msg_json))
    out_json = mongoutils.construct_json_from_query_list(out_json)

    return out_json

def delete(id=None):
    data_list, is_objectid, is_error, resp = get_data_list(id)
    if is_error:
        return resp

    if (is_objectid):
        coll_contribution.delete_one({cfg.FIELD_OBJECTID: ObjectId(id)})
        msg = {"name": str(id)}
        msg_json = jsonutils.create_log_json("Contribution", "DELETE", msg)
        logging.info("DELETE " + json.dumps(msg_json))
        return rs_handlers.entry_deleted('ID', id)

    # ToDo: use following line to delete using the other field than ObjectId
    # try:
    #     coll_contribution.delete_one({fld: id})
    #     msg = {fld: str(id)}
    #     msg_json = jsonutils.create_log_json("Contribution", "DELETE", msg)
    #     logging.info("DELETE " + json.dumps(msg_json))
    #     return rs_handlers.entry_deleted('name', id)
    # except:
    #     msg = {
    #         "reason": "Failed to delete. The dataset does not exist: " + str(id),
    #         "error": "Not Found: " + request.url,
    #     }
    #     msg_json = jsonutils.create_log_json("Contribution", "DELETE", msg)
    #     logging.error("DELETE " + json.dumps(msg_json))
    #     return rs_handlers.not_found(msg_json)

def capabilities():
    # this is an empty constructor for avoding capabilities serach connexion error
    pass

def capabilities_get():
    pass

def capabilities_post():
    pass

def capabilities_search():
    pass

def capabilities__search(id=None):
    pass

def talents():
    pass

def talents_get():
    pass

def talents__search():
    pass

def construct_capability(in_json):
    is_required_field = True
    error_required = ""
    try:
        error_required = "name"
        name = in_json["name"]
        error_required = "description"
        description = in_json["description"]
        error_required = "isOpenSource"
        isOpenSource = in_json["isOpenSource"]
        error_required = "deploymentDetails"
        deploymentLocation = in_json["deploymentDetails"]
        error_required = "version"
        version = in_json["version"]
        error_required = "healthCheckUrl"
        healthCheckUrl = in_json["healthCheckUrl"]
        error_required = "dataDeletionEndpointDetails"
        deploymentLocation = in_json["dataDeletionEndpointDetails"]
    except:
        msg = {
            "reason": "Some of the required field in capability is not provided: " + str(error_required),
            "error": "Bad Request: " + request.url,
        }
        msg_json = jsonutils.create_log_json("Contribution", "POST", msg)
        logging.error("POST " + json.dumps(msg_json))
        return None, None, msg_json

    # new installation of the app
    capability_dataset = Capability('')
    capability_dataset, restjson = datasetutils.update_capability_dataset_from_json(capability_dataset, in_json)

    return capability_dataset, restjson, None

def construct_contributors(in_json):
    # need to know if it is person or organization
    # TODO make better algorithm for this, but for now use if there is firstname or lastname it is a Person, otherwise, organization

    is_person = False
    try:
        firstname = in_json["firstName"]
        is_person = True
    except:
        pass
    try:
        lastname = in_json["lastName"]
        is_person = True
    except:
        pass

    contributor_dataset = None
    if is_person:
        contributor_dataset = Person('')
        contributor_dataset, restjson = datasetutils.update_person_dataset_from_json(contributor_dataset, in_json)
        # set affilication
        try:
            affilication_json = in_json['affiliation']
            affilication_dataset = Organization('')
            affilication_dataset, restjson = datasetutils.update_organization_dataset_from_json(affilication_dataset, affilication_json)
            contributor_dataset.set_affilication(affilication_dataset)
            del restjson['affiliation']
        except:
            pass
    else: # organization
        contributor_dataset = Organization('')
        contributor_dataset, restjson = datasetutils.update_organization_dataset_from_json(contributor_dataset, in_json)

    return contributor_dataset, restjson, None

def get_data_list(name):
    resp = None
    is_error = False

    if name != None:
        is_objectid = mongoutils.check_if_objectid(name)

        # query using either non-pii ObjectId or name
        if (is_objectid):
            id = ObjectId(name)
            db_data = mongoutils.query_dataset_by_objectid(coll_contribution, id)
        else:
            db_data = mongoutils.query_dataset(coll_contribution, cfg.FIELD_NAME, name)

        data_list = list(db_data)

        if len(data_list) > 1:
            msg = {
                "reason": "There are more than 1 contribution record: " + str(name),
                "error": "Bad Request: " + request.url,
            }
            msg_json = jsonutils.create_log_json("Contribution", "GET", msg)
            logging.error("GET " + json.dumps(msg_json))
            is_error = True
            resp = rs_handlers.bad_request(msg_json)
        elif len(data_list) == 0:
            msg = {
                "reason": "There is no contribution record: " + str(name),
                "error": "Not Found: " + request.url,
            }
            msg_json = jsonutils.create_log_json("Contribution", "GET", msg)
            logging.error("GET " + json.dumps(msg_json))
            is_error = True
            resp = rs_handlers.not_found(msg_json)

        return data_list, is_objectid, is_error, resp

    else:
        msg = {
            "reason": "The contribution does not exist: " + str(name),
            "error": "Not Found: " + request.url,
        }
        msg_json = jsonutils.create_log_json("Contribution", "GET", msg)
        logging.error("GET " + json.dumps(msg_json))
        resp = rs_handlers.not_found(msg_json)

    return None, None, True, resp
