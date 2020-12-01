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

from flask import current_app, g
import pymongo
import json
from pymongo.mongo_client import MongoClient
import controllers.configs as cfg

client = None


def get_db():
    if 'db' not in g:
        g.db = client.get_database(name=cfg.EVENT_DB_NAME)
    return g.db


def init_db():
    global client
    client = MongoClient(cfg.EVENT_MONGO_URL)

    # Create indexes on app start
    db = client.get_database(name=cfg.EVENT_DB_NAME)
    events = db['events']
    events.create_index([("title", pymongo.TEXT)])
    events.create_index([("startDate", pymongo.DESCENDING)])
    events.create_index([("endDate", pymongo.DESCENDING)])
    events.create_index([("sponsor", pymongo.ASCENDING)])
    events.create_index([("category", pymongo.ASCENDING)])
    events.create_index([("categorymainsub", pymongo.ASCENDING)])
    events.create_index([("coordinates", pymongo.GEOSPHERE)])

    # Add unique index on categories collection
    categories = db['categories']
    categories.create_index("category", unique=True)

    # Insert categories collection data.
    with open('api/categories.json') as file:
        json_data = json.load(file)
        for record in json_data:
            try:
                categories.insert(record)
            except pymongo.errors.DuplicateKeyError:
                continue
