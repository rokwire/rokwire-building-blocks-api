import controllers.config as cfg
import pymongo
from flask import g
from pymongo.mongo_client import MongoClient

client = None


def get_db():
    if 'db' not in g:
        g.db = client.get_database(cfg.APP_CONFIG_DB_NAME)
    return g.db


def init_db():
    global client
    client = MongoClient(cfg.APP_CONFIG_MONGO_URL)

    # Create indexes on api start
    db = client.get_database(name=cfg.APP_CONFIG_DB_NAME)
    app_configs = db[cfg.APP_CONFIGS_COLLECTION]
    app_configs.create_index([("mobileAppVersion", pymongo.DESCENDING)], unique=True)
