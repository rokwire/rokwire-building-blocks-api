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
API_LOC = os.getenv('API_LOC', '../../')

DEBUG = bool(os.getenv('DEBUG', 'False') == 'True')
