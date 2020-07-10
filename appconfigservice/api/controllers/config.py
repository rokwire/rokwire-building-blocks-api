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

APP_CONFIG_MONGO_URL = os.getenv('APP_CONFIG_MONGO_URL', 'mongodb://localhost:27017')
APP_CONFIG_DB_NAME = 'app_config_db'
APP_CONFIG_MAX_POOLSIZE = 100,
APP_CONFIG_URL_PREFIX = os.getenv('APP_CONFIG_URL_PREFIX', '')
APP_CONFIGS_COLLECTION = 'app_configs'

API_LOC = os.getenv('API_LOC', '../')
# APP_CONFIG_ENDPOINT = os.getenv('APPCONFIG_ENDPOINT', '/rest_service')
DEBUG = bool(os.getenv('DEBUG', 'False') == 'True')
