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
import ast
from dotenv import load_dotenv

# Load .env file
load_dotenv()

API_LOC = os.getenv('API_LOC', '../')
DEBUG = bool(os.getenv('DEBUG', 'False') == 'True')

EVENT_MONGO_URL = os.getenv("EVENT_MONGO_URL", "mongodb://localhost:27017")
EVENT_DB_NAME = os.getenv("EVENT_DB_NAME", "rokwire")
# set default as empty, since connexion will set events as the root path defined by the yml file.
URL_PREFIX = os.getenv("URL_PREFIX", "")

GROUPS_BUILDING_BLOCK_HOST= os.getenv("GROUPS_BUILDING_BLOCK_HOST", "https://api-dev.rokwire.illinois.edu/gr")
ROKWIRE_AUTH_HOST = os.getenv("ROKWIRE_AUTH_HOST", "https://api-dev.rokwire.illinois.edu/core")
SHIB_HOST = os.getenv("SHIB_HOST", "shibboleth.illinois.edu")

ROKWIRE_GROUPS_API_KEY = os.getenv("ROKWIRE_GROUPS_API_KEY", "")

IMAGE_COLLECTION = os.getenv("IMAGE_COLLECTION", "images")
IMAGE_FILE_MOUNTPOINT = os.getenv("IMAGE_FILE_MOUNTPOINT", "events-images")
IMAGE_URL = os.getenv("IMAGE_URL", "https://{bucket}.s3-{region}.amazonaws.com/{prefix}/{event_id}/{image_id}.jpg")
MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", "4194304"))  # 4 * 1024 * 1024
ALLOWED_EXTENSIONS = ast.literal_eval(os.getenv("ALLOWED_EXTENSIONS", "{'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}"))

AWS_IMAGE_FOLDER_PREFIX = os.getenv("AWS_IMAGE_FOLDER_PREFIX", "events")
BUCKET = os.getenv("AWS_S3_BUCKET", "rokwire-events-s3-images")
