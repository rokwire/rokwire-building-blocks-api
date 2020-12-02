#  Copyright 2020 Board of Trustees of the University of Illinois.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import json
import datetime
import logging
import uuid as uuidlib
import copy

from flask import jsonify, request, g
from bson import ObjectId

import controllers.configs as cfg
import utils.mongoutils as mongoutils
import utils.jsonutils as jsonutils
import utils.datasetutils as datasetutils
import utils.rest_handlers as rs_handlers
import utils.otherutils as otherutils
import utils.tokenutils as tokenutils
import utils.mongoutils as mongoutils

from utils import query_params
from models.pii_data import PiiData
from models.non_pii_data import NonPiiData
from models.testresultsconsent import TestResultsConsent

def get(clientid=None,uuid=None):
    print("test")
