import io
import os
import json
import logging
import flask
import flask.json
import auth_middleware
import pymongo

from bson import ObjectId

def search():
    print("Test")