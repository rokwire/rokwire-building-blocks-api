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
from pymongo import MongoClient, ASCENDING

import utils.jsonutils as jsonutils

client_profile = MongoClient(cfg.EVENT_MONGO_URL, connect=False)
db_event = client_profile[cfg.EVENT_DB_NAME]

"""
get query output json of PII from query using search arguments
"""

"""
insert non pii dataset to mognodb
"""
def insert_event_to_mongodb(dataset):
    id = db_event["event"].insert(dataset)

    return dataset, id
