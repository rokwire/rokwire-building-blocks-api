import os

from dotenv import load_dotenv

# Load .env file
load_dotenv()

# this has to be have the file path to the folder for saving image files and other necessary files from rest service
PROFILE_REST_STORAGE = os.getenv('REST_STORAGE', '/usr/src/app/rest')
MONGO_PROFILE_URL = os.getenv('MONGO_PROFILE_URL', 'localhost:27017')
MONGO_PII_URL = os.getenv('MONGO_PII_URL', 'localhost:27017')
FLASK_APP = os.getenv('FLASK_APP', 'profile_rest_service')
FLASK_ENV = os.getenv('FLASK_ENV', 'production')
API_LOC = os.getenv('API_LOC', '../../')
PROFILE_URL_PREFIX = os.getenv('PROFILE_URL_PREFIX', '')
DEBUG = bool(os.getenv('DEBUG', 'False') == 'True')

PROFILE_DB_NAME = 'profiledb'
PII_DB_NAME = 'piidb'
PROFILE_DB_PROFILE_COLL_NAME = 'NonPiiDataset'
PII_DB_PII_COLL_NAME = 'PiiDataset'
FIELD_OBJECTID = '_id'
FIELD_PROFILE_UUID = 'uuid'
FIELD_PID = 'pid'