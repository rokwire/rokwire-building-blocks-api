#  Copyright 2021 Board of Trustees of the University of Illinois.
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
#
from utils import jsonutil
import json

from controllers.config import Config as cfg

from flask import json
from bson.json_util import dumps
from pymongo import MongoClient, ASCENDING

client_contribution = MongoClient(cfg.MONGO_URL, connect=False)
db_contribution = client_contribution[cfg.CONTRIBUTION_DB_NAME]
coll_contribution = db_contribution[cfg.CONTRIBUTION_COLL_NAME]
coll_contribution.create_index([("name", ASCENDING)], background=True)
coll_contribution.create_index([("capabilities.name", ASCENDING)], background=True)
coll_contribution.create_index([("talents.name", ASCENDING)], background=True)

coll_reviewer = db_contribution[cfg.REVIEWER_COLL_NAME]
coll_reviewer.create_index([("name", ASCENDING)], background=True)

"""
get json of all the reviewers list
"""
def list_reviewers():
    db_data = coll_reviewer.find({})
    data_list = list(db_data)

    if len(data_list) > 0:
        data_dump = dumps(data_list)
        json_load = json.loads(data_dump)
        json_load = jsonutil.convert_obejctid_from_dataset_json_list(json_load)

        return json_load
    else:
        return None