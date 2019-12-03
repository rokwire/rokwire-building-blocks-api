import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

APP_CONFIG_MONGO_URL = os.getenv('APP_CONFIG_MONGO_URL', 'mongodb://localhost:27017')
APP_CONFIG_DB_NAME = 'app_config_db'
APP_CONFIG_MAX_POOLSIZE = 100,
APP_CONFIGS_COLLECTION = 'app_configs'
API_LOC = os.getenv('API_LOC', '../../')
# APP_CONFIG_ENDPOINT = os.getenv('APPCONFIG_ENDPOINT', '/rest_service')
DEBUG = os.getenv('DEBUG', 'False')