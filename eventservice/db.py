from flask import current_app, g
from pymongo.mongo_client import MongoClient

# FIXME! Next 2 lines added for debugging
EVENT_MONGO_URL = "mongodb://localhost:27017"
EVENT_DB_NAME = "eventdb"

def get_db():
    if 'db' not in g:
        # FIXME! next 2 lines need to be uncommented and following 2 removed!
        # g.client = MongoClient(current_app.config['EVENT_MONGO_URL'])
        # g.db = g.client.get_database(name=current_app.config['EVENT_DB_NAME'])
        g.client = MongoClient(EVENT_MONGO_URL)
        g.db = g.client.get_database(name=EVENT_DB_NAME)
    return g.db

def close_db(e=None):
    client = g.pop('client', None)

    if client is not None:
        client.close()


def init_app(app):
    app.teardown_appcontext(close_db)
