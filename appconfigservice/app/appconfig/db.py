from flask import current_app, g
from pymongo.mongo_client import MongoClient
import pymongo


def get_db():
    if 'db' not in g:
        g.client = MongoClient(current_app.config['APP_CONFIG_MONGO_URL'])
        g.db = g.client.get_database(name=current_app.config['APP_CONFIG_DB_NAME'])
        g.collection = g.db[current_app.config['APP_CONFIGS_COLLECTION']]
        g.collection.create_index([("mobileAppVersion", pymongo.DESCENDING)], unique=True)
    return g.db


def close_db(e=None):
    client = g.pop('client', None)

    if client is not None:
        client.close()


def init_app(app):
    app.teardown_appcontext(close_db)
