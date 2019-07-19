from flask import current_app, g
from pymongo.mongo_client import MongoClient


def get_db():
    if 'db' not in g:
        if 'client' not in g:
            g.client = MongoClient(current_app.config['EVENT_MONGO_URL'])
        g.db = g.client.get_database(name=current_app.config['EVENT_DB_NAME'])
    return g.db

def get_imagedb():
    if 'imagedb' not in g:
        if 'client' not in g:
            g.client = MongoClient(current_app.config['EVENT_MONGO_URL'])
        g.imagedb = g.client.get_database(name=current_app.config['IMAGE_DB_NAME'])
    return g.imagedb

def close_db(e=None):
    client = g.pop('client', None)

    if client is not None:
        client.close()


def init_app(app):
    app.teardown_appcontext(close_db)
