from flask import current_app, g
from pymongo.mongo_client import MongoClient
import pymongo

client = None

def get_db():
    if 'db' not in g:
        g.db = client.get_database(name=current_app.config['APP_CONFIG_DB_NAME'])
    return g.db


def init_db(app):
    global client
    client = MongoClient(app.config['APP_CONFIG_MONGO_URL'])

    # Create indexes on api start
    db = client.get_database(name=app.config['APP_CONFIG_DB_NAME'])
    app_configs = db[app.config['APP_CONFIGS_COLLECTION']]
    app_configs.create_index([("mobileAppVersion", pymongo.DESCENDING)], unique=True)
