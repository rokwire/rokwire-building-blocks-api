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
load_dotenv(verbose=True)

# this has to be have the file path to the folder for saving image files and other necessary files from rest service
# LOGGING_MONGO_URL = os.getenv('LOGGING_MONGO_URL', 'mongodb://localhost:27017')
# LOGGING_DB_NAME="loggingdb"
# LOGGING_COLL_NAME="logs"
LOGGING_URL_PREFIX = os.getenv('LOGGING_URL_PREFIX', '')
FLASK_APP = os.getenv('FLASK_APP', 'logging_rest_service')
FLASK_ENV = os.getenv('FLASK_ENV', 'production')
API_LOC = os.getenv('API_LOC', '../')
PRINT_LOG = bool(os.getenv('PRINT_LOG', 'True') == 'True')

DEBUG = bool(os.getenv('DEBUG', 'False') == 'True')

VERSION = '1.13.0'