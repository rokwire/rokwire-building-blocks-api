from flask import current_app, g
from pymongo.mongo_client import MongoClient

client = None

def get_db():
    if 'db' not in g:
        g.db = client.get_database(name=current_app.config['LOGGING_DB_NAME'])
    return g.db


def init_db(app):
    global client

    if app.config.get('LOGGING_MONGO_URL', None):
        client = MongoClient(app.config['LOGGING_MONGO_URL'])
