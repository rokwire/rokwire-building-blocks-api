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

import connexion
import pytest
from controllers.config import API_LOC
from flask import current_app
# import .controllers.config as cfg
from rokwireresolver import RokwireResolver

from ..utils import db as conn


@pytest.fixture
def app():
    """Create and configure a new api instance for each test."""
    app = connexion.FlaskApp(__name__, specification_dir=API_LOC)
    app.add_api('appconfig.yaml', arguments={'title': 'Rokwire'}, resolver=RokwireResolver('controllers'),
                resolver_error=501)
    yield app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


def test_post_app_config(client, app):
    """Test POST API"""
    req_data = {
        "mobileAppVersion": "0.1.0",
        "platformBuildingBlocks": {},
        "thirdPartyServices": {},
        "otherUniversityServices": {},
        "secretKeys": "blabla",
        "upgrade": {}
    }
    assert client.post('/app/configs', data=json.dumps(req_data), content_type='application/json').status_code == 201
    with app.app_context():
        db = conn.get_db()
        config = db[current_app.config['APP_CONFIGS_COLLECTION']].find_one({'mobileAppVersion': '0.1.0'})
        assert config['mobileAppVersion'] == '0.1.0'


def test_update_app_config(client, app):
    """Test PUT API"""
    id = None
    with app.app_context():
        db = conn.get_db()
        config = db[current_app.config['APP_CONFIGS_COLLECTION']].find_one({'mobileAppVersion': '0.1.0'})
        id = config['_id']
    new_data = {
        "mobileAppVersion": "0.1.0",
        "platformBuildingBlocks": {
            "events": "https://api-dev.rokwire.illinois.edu/events",
            "profiles": "https://api-dev.rokwire.illinois.edu/profiles",
            "appconfigs": "https://api-dev.rokwire.illinois.edu/app/configs"
        },
        "thirdPartyServices": {},
        "otherUniversityServices": {},
        "secretKeys": "blabla",
        "upgrade": {
            "available_version": "0.1.1",
            "required_version": "0.1.0",
            "url": {
                "android": "market://details?id=com.dropbox.android",
                "ios": "itms-apps://itunes.apple.com/us/app/apple-store/id327630330"}
        }
    }
    if id is not None:
        assert client.put('/app/configs/' + str(id), data=json.dumps(new_data),
                          content_type='application/json').status_code == 200
    with app.app_context():
        db = conn.get_db()
        config = db[current_app.config['APP_CONFIGS_COLLECTION']].find_one({'mobileAppVersion': '0.1.0'})
        assert config['platformBuildingBlocks']['appconfigs'] == 'https://api-dev.rokwire.illinois.edu/app/configs'


def test_get_app_config(client, app):
    """Test GET API given mobile app version"""
    assert client.get('/app/configs?mobileAppVersion=0.1.0').status_code == 200
    response = client.get('/app/configs')
    assert b'0.1.0' in response.data


def test_get_app_config_by_id(client, app):
    """Test GET API given an app config identifier"""
    id = None
    with app.app_context():
        db = conn.get_db()
        config = db[current_app.config['APP_CONFIGS_COLLECTION']].find_one({'mobileAppVersion': '0.1.0'})
        id = config['_id']
    if id is not None:
        resp = client.get('/app/configs/' + str(id))
        assert resp.status_code == 200
        assert b'0.1.0' in resp.data


def test_secret_key(client, app):
    """Test GET API given mobile app version"""
    response = client.get('/app/configs?mobileAppVersion=0.1.0')
    assert b'blahblah' in response.data


def test_delete_app_config(client, app):
    """Test DELETE API"""
    id = None
    with app.app_context():
        db = conn.get_db()
        for doc in db[current_app.config['APP_CONFIGS_COLLECTION']].find({'mobileAppVersion': '0.1.0'}):
            id = doc['_id']
            if id is not None:
                resp = client.delete('/app/configs/' + str(id))
                assert (resp.status_code == 202)
