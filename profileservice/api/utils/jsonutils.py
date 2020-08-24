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

from flask import make_response

def remove_objectid_from_dataset(dataset):
    if "_id" in dataset:
        del dataset["_id"]

    return dataset

def remove_file_descriptor_from_dataset(dataset):
    if "fileDescriptors" in dataset:
        del dataset["fileDescriptors"]

    return dataset

def remove_file_descriptor_from_data_list(data_list):
    for i in range(len(data_list)):
        del data_list[i]["fileDescriptors"]

    return data_list

def remove_null_subcategory(injson):
    interests = injson["interests"]
    for i in range(len(interests)):
        interest = interests[i]
        subcategories = interest["subcategories"]
        if subcategories is None:
            del interest['subcategories']

    return injson

def create_log_json(ep_name, ep_method, in_json):
    in_json['ep_building_block'] = "profile_building_block"
    in_json['ep_name'] = ep_name
    in_json['ep_method'] = ep_method

    return in_json

def create_auth_fail_message():
    out_json = make_response("{\"Authorization Failed\": \"The user info in id token and db are not matching.\"}")
    out_json.mimetype = 'application/json'
    out_json.status_code = 403

    return out_json