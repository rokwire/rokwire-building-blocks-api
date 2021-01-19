import os


class Config(object):
    CONTRIBUTION_BUILDING_BLOCK_URL = os.getenv("CONTRIBUTION_BUILDING_BLOCK_URL",
                                                "http://localhost:5000/contributions")
    MONGO_URL = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
    DB_NAME = os.getenv("MONGO_DATABASE", "contribution")
    DB_COLLECTION = os.getenv("MONGO_DATABASE", "catalog")

    URL_PREFIX = os.getenv("URL_PREFIX", "")

    DBTYPE = 'mongoDB'
    SECRET_KEY = os.getenv("SECRET_KEY", "SECRET_KEY")
    AUTHENTICATION_TOKEN = os.getenv("AUTHENTICATION_TOKEN", "...")
    ROKWIRE_API_KEY = os.getenv("ROKWIRE_API_KEY", "...")
    DEBUG = True

    client_id = os.getenv("CLIENT_ID", "NO ID")
    client_secret = os.getenv("CLIENT_SECRET", "NO SECRET")
    authorization_base_url = 'https://github.com/login/oauth/authorize'
    token_url = 'https://github.com/login/oauth/access_token'