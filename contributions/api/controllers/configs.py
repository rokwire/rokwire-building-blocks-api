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

import os

from dotenv import load_dotenv

# Load .env file
load_dotenv()

# this has to be have the file path to the folder for saving image files and other necessary files from rest service
MONGO_CONTRIBUTION_URL = os.getenv('MONGO_CONTRIBUTION_URL', 'localhost:27017')
FLASK_APP = os.getenv('FLASK_APP', 'contribution_rest_service')
FLASK_ENV = os.getenv('FLASK_ENV', 'production')
API_LOC = os.getenv('API_LOC', '../')
CONTRIBUTION_URL_PREFIX = os.getenv('CONTRIBUTION_URL_PREFIX', '')
DEBUG = bool(os.getenv('DEBUG', 'False') == 'True')
CORS_ENABLED = bool(os.getenv('CORS_ENABLED', 'False') == 'True')

CONTRIBUTION_DB_NAME = os.getenv('CONTRIBUTION_DB_NAME', 'contributions_db')
CONTRIBUTION_COLL_NAME = os.getenv('CONTRIBUTION_COLL_NAME', 'contributions')
REVIEWER_COLL_NAME = os.getenv('REVIEWER_COLL_NAME', 'reviewers')

FIELD_OBJECTID = '_id'
FIELD_NAME = 'name'

ADMIN_USERS = os.getenv('ADMIN_USERS', '')

SENDER_EMAIL = os.getenv('SENDER_EMAIL', '')
SENDER_EMAIL_PASSWORD = os.getenv('SENDER_EMAIL_PASSWORD', '')
