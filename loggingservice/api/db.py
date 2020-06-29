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
from pymongo.mongo_client import MongoClient

client = None

def get_db():
    if 'db' not in g:
        g.db = client.get_database(name=current_app.config['LOGGING_DB_NAME'])
    return g.db


def init_db(app):
    global client

    if app.config.get('LOGGING_MONGO_URL', None):
        client = MongoClient(app.config['LOGGING_MONGO_URL'])
