import os
from datetime import timedelta


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


    # # ADMINS defines a list usernames that serve as administrators
    # ADMINS = []
    #
    # # OIDC CONFIG FOR LOGIN
    # ISSUER_URL = os.getenv("ISSUER_URL", "https://shibboleth-test.techservices.illinois.edu")  # test instance
    # SCOPES = os.getenv("SCOPES",
    #                    ["openid", "profile", "email", "offline_access"])  # Other OIDC scopes can be added as needed.
    # REDIRECT_URIS = os.getenv("REDIRECT_URIS", "")
    # CLIENT_ID = os.getenv("CLIENT_ID", "")
    # CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
    #
    # # LOGIN_MODE SELECTED
    # LOGIN_MODE = os.getenv("LOGIN_MODE", "shibboleth")  # TODO: Add an option "local" for local login.
    #
    # # ROLE OF USERS
    # ROLE = {
    # }
    #
    # # SESSION EXPIRATION TIME
    # PERMANENT_SESSION_LIFETIME = timedelta(hours=os.getenv("SESSION_LIFETIME_IN_HOURS", 1))
