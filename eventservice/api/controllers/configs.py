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
ROKWIRE_ISSUER = os.getenv('ROKWIRE_ISSUER', 'https://api.rokwire.illinois.edu/')

ROKWIRE_GROUPS_API_KEY = os.getenv("ROKWIRE_GROUPS_API_KEY", "")

IMAGE_COLLECTION = os.getenv("IMAGE_COLLECTION", "images")
IMAGE_FILE_MOUNTPOINT = os.getenv("IMAGE_FILE_MOUNTPOINT", "events-images")
IMAGE_URL = os.getenv("IMAGE_URL", "https://{bucket}.s3-{region}.amazonaws.com/{prefix}/{event_id}/{image_id}.jpg")
MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", "4194304"))  # 4 * 1024 * 1024
ALLOWED_EXTENSIONS = ast.literal_eval(os.getenv("ALLOWED_EXTENSIONS", "{'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}"))

AWS_IMAGE_FOLDER_PREFIX = os.getenv("AWS_IMAGE_FOLDER_PREFIX", "events")
BUCKET = os.getenv("AWS_S3_BUCKET", "rokwire-events-s3-images")

ERR_MSG_GET_GROUP_MEMBERSHIP = os.getenv("ERR_MSG_GET_GROUP_MEMBERSHIP", "failed to verify group membership.")
ERR_MSG_GET_EVENT = os.getenv("ERR_MSG_GET_EVENT", "failed to get event.")
ERR_MSG_GET_IMG = os.getenv("ERR_MSG_GET_IMG", "failed to check existing image.")
ERR_MSG_GET_GROUP = os.getenv("ERR_MSG_GET_GROUP", "failed to get group.")
ERR_MSG_GET_IMG_FILE = os.getenv("ERR_MSG_GET_IMG_FILE", "failed to get image.")
ERR_MSG_GET_COORDINATE = os.getenv("ERR_MSG_GET_COORDINATE", "failed to get coordinate.")
ERR_MSG_UPDATE = os.getenv("ERR_MSG_UPDATE", "event update failed.")
ERR_MSG_PATCH_EVENT = os.getenv("ERR_MSG_PATCH_EVENT", "failed to patch the event.")
ERR_MSG_DELETE_EVENT = os.getenv("ERR_MSG_DELETE_EVENT", "failed to delete event.")
ERR_MSG_DELETE_IMG = os.getenv("ERR_MSG_DELETE_IMG", "failed to delete image.")
ERR_MSG_SEARCH_TAG = os.getenv("ERR_MSG_SEARCH_TAG", "tag search failed.")
ERR_MSG_SEARCH_SUPERTAG = os.getenv("ERR_MSG_SEARCH_SUPERTAG", "super event tag search failed.")
ERR_MSG_SEARCH_CATEGORY = os.getenv("ERR_MSG_SEARCH_CATEGORY", "category search failed.")
ERR_MSG_POST_EVENT = os.getenv("ERR_MSG_POST_EVENT", "event creation failed.")
ERR_MSG_POST_IMG = os.getenv("ERR_MSG_POST_IMG", "failed to post image.")