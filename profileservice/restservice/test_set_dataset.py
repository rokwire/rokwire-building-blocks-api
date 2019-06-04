import json
import hashlib
import os
import shutil
import tempfile

import json
from bson import ObjectId
from mimetypes import MimeTypes
from pymongo import MongoClient
from urllib.request import urlretrieve
from profileservice.dao.non_pii_data import non_pii_data
from profileservice.dao.pii_data import pii_data

def main():
    filename = 'test_json.json'
    mongo_url = "mongodb://localhost"
    with open(filename, "r") as profile_txt:
        profile_json = json.load(profile_txt)

    profile = non_pii_data(profile_json)
    id = insert_profile_to_mongodb(mongo_url, profile)
    print(id)

def insert_profile_to_mongodb(mongo_url, indataset):
    client = MongoClient(mongo_url, 27017)
    db = client['profiledb']
    coll = db.ProfileDataset

    dataset = json.dumps(indataset, default=lambda x: x.__dict__)
    dataset = json.loads(dataset)

    id = coll.insert(dataset)

    return id

if __name__ == "__main__":
    main()