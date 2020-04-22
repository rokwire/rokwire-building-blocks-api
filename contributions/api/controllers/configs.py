import os

from dotenv import load_dotenv

# Load .env file
load_dotenv()

# this has to be have the file path to the folder for saving image files and other necessary files from rest service
MONGO_CONTRIBUTION_URL = os.getenv('MONGO_CONTRIBUTION_URL', 'localhost:27017')
FLASK_APP = os.getenv('FLASK_APP', 'contribution_rest_service')
FLASK_ENV = os.getenv('FLASK_ENV', 'production')
API_LOC = os.getenv('API_LOC', '../../')
CONTRIBUTION_URL_PREFIX = os.getenv('CONTRIBUTION_URL_PREFIX', '')
DEBUG = bool(os.getenv('DEBUG', 'False') == 'True')

CONTRIBUTION_DB_NAME = 'contributiondb'
CONTRIBUTION_COLL_NAME = 'contributions'
CAPABILITY_COLL_NAME = 'capabilities'
FIELD_OBJECTID = '_id'
FIELD_NAME = 'name'