from flask import current_app, g
from pymongo.mongo_client import MongoClient


def get_db():
    if 'db' not in g:
        g.client = MongoClient(current_app.config['LOGGING_MONGO_URL'])
        g.db = g.client.get_database(name=current_app.config['LOGGING_DB_NAME'])
    return g.db


def close_db(e=None):
    client = g.pop('client', None)

    if client is not None:
        client.close()


def init_app(app):
    app.teardown_appcontext(close_db)
