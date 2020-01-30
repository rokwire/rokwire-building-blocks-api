from flask import current_app, g
import pymongo
from pymongo.mongo_client import MongoClient
import controllers.configs as cfg

client = None


def get_db():
    if 'db' not in g:
        g.db = client.get_database(name=cfg.EVENT_DB_NAME)
    return g.db


def init_db():
    global client
    client = MongoClient(cfg.EVENT_MONGO_URL)

    # Create indexes on app start
    db = client.get_database(name=cfg.EVENT_DB_NAME)
    events = db['events']
    events.create_index([("title", pymongo.TEXT)])
    events.create_index([("startDate", pymongo.DESCENDING)])
    events.create_index([("endDate", pymongo.DESCENDING)])
    events.create_index([("sponsor", pymongo.ASCENDING)])
    events.create_index([("category", pymongo.ASCENDING)])
    events.create_index([("categorymainsub", pymongo.ASCENDING)])
    events.create_index([("coordinates", pymongo.GEOSPHERE)])
