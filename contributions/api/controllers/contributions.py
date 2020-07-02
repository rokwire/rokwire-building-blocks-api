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
import datetime
import logging
import copy

from flask import jsonify, request, g
from bson import ObjectId

import controllers.configs as cfg
import utils.jsonutils as jsonutils
import utils.datasetutils as datasetutils
import utils.rest_handlers as rs_handlers
import utils.mongoutils as mongoutils

from utils import query_params
from models.contribution import Contribution
from models.person import Person
from models.organization import Organization
from models.capabilities.capability import Capability
from models.talents.talent import Talent
from pymongo import MongoClient

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

        # set talent list
        talent_list = []
        try:
            talent_json = in_json["talents"]
            for i in range(len(talent_json)):
                talent, rest_takebt_json, msg = construct_talent(talent_json[i])
                if talent is None:
                    return rs_handlers.bad_request(msg)
                talent_list.append(talent)
            contribution_dataset.set_talents(talent_list)
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

def get(id):
    data_list, is_objectid, is_error, resp = get_data_list(id)
    if is_error:
        return resp
    jsonutils.remove_objectid_from_dataset(data_list[0])
    out_json = mongoutils.construct_json_from_query_list(data_list[0])
    msg_json = jsonutils.create_log_json("Contribution", "GET", data_list[0])
    logging.info("Contribution GET " + json.dumps(jsonutils.remove_objectid_from_dataset(msg_json)))

    return out_json

def put(id):
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

    if contribution_dataset is None:
        msg = {
            "reason": "There is no contribution dataset with given id: " + str(id),
            "error": "Not Found: " + request.url,
        }
        msg_json = jsonutils.create_log_json("Contribution", "PUT", msg)
        logging.error("PUT " + json.dumps(msg_json))
        return rs_handlers.not_found(msg_json)

    date_created = contribution_dataset.dateCreated
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

    out_json = contribution_dataset
    msg_json = jsonutils.create_log_json("Contribution", "PUT", copy.copy(out_json))
    logging.info("PUT " + json.dumps(msg_json))
    out_json = mongoutils.construct_json_from_query_list(out_json)

    return out_json

def delete(id):
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

def allcapabilitiessearch():
    args = request.args
    query = dict()
    try:
        query = query_params.format_query_capability(args, query)
    except Exception as ex:
        msg = {
            "reason": "The query is wrong or bad argument " + str(args),
            "error": "Bad Request: " + request.url,
        }
        msg_json = jsonutils.create_log_json("Capability", "SEARCH", msg)
        logging.error("Capability SEARCH " + json.dumps(msg_json))
        return rs_handlers.bad_request(msg_json)

    try:
        out_json = mongoutils.get_result(coll_contribution, query)
    except Exception as ex:
        msg = {
            "reason": "The query is wrong or bad argument " + str(args),
            "error": "Bad Request: " + request.url,
        }
        msg_json = jsonutils.create_log_json("Capability", "SEARCH", msg)
        logging.error("Capability SEARCH " + json.dumps(msg_json))
        return rs_handlers.bad_request(msg_json)

    return_json = []
    if out_json is None:
        return_json = []
    else:   # extract out capabilities with the given name
        if isinstance(out_json, list):
            for tmp_json in out_json:
                capabilities_json = tmp_json["capabilities"]
                # TODO this is the case of only 1 args that is name.
                #  If there are more args this should be updated
                for tmp_capability_json in capabilities_json:
                    capability_json = None
                    if tmp_capability_json["name"] == args["name"]:
                        capability_json = tmp_capability_json
                        return_json.append(capability_json)
        else:
            capabilities_json = out_json["capabilities"]
            # TODO this is the case of only 1 args that is name.
            #  If there are more args this should be updated
            for tmp_capability_json in capabilities_json:
                capability_json = None
                if tmp_capability_json["name"] == args["name"]:
                    capability_json = tmp_capability_json
                    return_json.append(capability_json)
    msg = {
        "search": "Capability search performed with arguments of : " + str(args),
        "result": return_json,
    }
    msg_json = jsonutils.create_log_json("Capability", "SEARCH", msg)
    logging.info("Capability SEARCH " + json.dumps(msg_json))

    return return_json

def capabilities_search(id):
    try:
        contribution_dataset = mongoutils.get_contribution_dataset_from_objectid(coll_contribution, id)
        capability_dataset = contribution_dataset.get_capabilities()
    except Exception as ex:
        msg = {
            "reason": "There is no contribution dataset with given id: " + str(id),
            "error": "Not Found: " + request.url,
        }
        msg_json = jsonutils.create_log_json("Capability", "SEARCH", msg)
        logging.error("Capability SEARCH " + json.dumps(msg_json))
        return rs_handlers.bad_request(msg_json)

    if capability_dataset is None:
        msg = {
            "reason": "There is no capability with given contribution id: " + str(id),
            "error": "Not Found: " + request.url,
        }
        msg_json = jsonutils.create_log_json("Capability", "GET", msg)
        logging.error("Capability SEARCH " + json.dumps(msg_json))
        return rs_handlers.not_found(msg_json)

    msg = {
        "search": "Capability data in the contirubion dataset with given id : " + str(id),
        "result": capability_dataset,
    }
    msg_json = jsonutils.create_log_json("Capability", "SEARCH", msg)
    logging.info("Capability SEARCH " + json.dumps(msg))

    return capability_dataset

def alltalentssearch():
    args = request.args
    query = dict()
    try:
        query = query_params.format_query_talent(args, query)
    except Exception as ex:
        msg = {
            "reason": "The query is wrong or bad argument " + str(args),
            "error": "Bad Request: " + request.url,
        }
        msg_json = jsonutils.create_log_json("Talent", "SEARCH", msg)
        logging.error("Talent SEARCH " + json.dumps(msg_json))
        return rs_handlers.bad_request(msg_json)

    try:
        out_json = mongoutils.get_result(coll_contribution, query)
    except Exception as ex:
        msg = {
            "reason": "The query is wrong or bad argument " + str(args),
            "error": "Bad Request: " + request.url,
        }
        msg_json = jsonutils.create_log_json("Talent", "SEARCH", msg)
        logging.error("Talent SEARCH " + json.dumps(msg_json))
        return rs_handlers.bad_request(msg_json)

    return_json = []
    if out_json is None:
        return_json = []
    else:   # extract out talent with the given name
        if isinstance(out_json, list):
            for tmp_json in out_json:
                talents_json = tmp_json["talents"]
                # TODO this is the case of only 1 args that is name.
                #  If there are more args this should be updated
                for tmp_talent_json in talents_json:
                    talent_json = None
                    if tmp_talent_json["name"] == args["name"]:
                        talent_json = tmp_talent_json
                        return_json.append(talent_json)
        else:
            talents_json = out_json["capabilities"]
            # TODO this is the case of only 1 args that is name.
            #  If there are more args this should be updated
            for tmp_talent_json in talents_json:
                talent_json = None
                if tmp_talent_json["name"] == args["name"]:
                    talent_json = tmp_talent_json
                    return_json.append(talent_json)
    msg = {
        "search": "Talent search performed with arguments of : " + str(args),
        "result": return_json,
    }
    msg_json = jsonutils.create_log_json("Talent", "SEARCH", msg)
    logging.info("Talent SEARCH " + json.dumps(msg_json))

    return return_json

def talents_search(id):
    try:
        contribution_dataset = mongoutils.get_contribution_dataset_from_objectid(coll_contribution, id)
        talent_dataset = contribution_dataset.get_talents()
    except Exception as ex:
        msg = {
            "reason": "There is no contribution dataset with given id: " + str(id),
            "error": "Not Found: " + request.url,
        }
        msg_json = jsonutils.create_log_json("Talent", "SEARCH", msg)
        logging.error("Talent SEARCH " + json.dumps(msg_json))
        return rs_handlers.bad_request(msg_json)

    if talent_dataset is None:
        msg = {
            "reason": "There is no Talent with given contribution id: " + str(id),
            "error": "Not Found: " + request.url,
        }
        msg_json = jsonutils.create_log_json("Talent", "GET", msg)
        logging.error("Talent SEARCH " + json.dumps(msg_json))
        return rs_handlers.not_found(msg_json)

    msg = {
        "search": "Talent data in the contirubion dataset with given id : " + str(id),
        "result": talent_dataset,
    }
    msg_json = jsonutils.create_log_json("Talent", "SEARCH", msg)
    logging.info("Talent SEARCH " + json.dumps(msg))

    return talent_dataset

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

def construct_talent(in_json):
    is_required_field = True
    error_required = ""
    try:
        error_required = "name"
        name = in_json["name"]
        error_required = "shortDescription"
        description = in_json["shortDescription"]
    except:
        msg = {
            "reason": "Some of the required field in talent is not provided: " + str(error_required),
            "error": "Bad Request: " + request.url,
        }
        msg_json = jsonutils.create_log_json("Contribution", "POST", msg)
        logging.error("POST " + json.dumps(msg_json))
        return None, None, msg_json

    # new installation of the app
    talent_dataset = Talent('')
    talent_dataset, restjson = datasetutils.update_talent_dataset_from_json(talent_dataset, in_json)

    return talent_dataset, restjson, None

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
