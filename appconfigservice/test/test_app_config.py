import pytest
import json
from flask import current_app

from appconfig import create_app
from appconfig import db as conn

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app({
        "APP_CONFIG_MONGO_URL": "mongodb://localhost:27017",
        "APP_CONFIG_DB_NAME": "app_config_db",
        "APP_CONFIG_MAX_POOLSIZE":  100,
        "APP_CONFIGS_COLLECTION": "app_configs"
    })
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
        "otherUniversityServices": {}
    }
    assert client.post('/app/configs', data=json.dumps(req_data), content_type='application/json').status_code == 201
    with app.app_context():
        db = conn.get_db()
        config = db[current_app.config['APP_CONFIGS_COLLECTION']].find_one({'mobileAppVersion': '0.1.0'})
        assert config['mobileAppVersion'] == '0.1.0'
        assert config['version_numbers'] == {'major': 0, 'minor': 1, 'patch': 0}

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
        "otherUniversityServices": {}
    }
    if id is not None:
        assert client.put('/app/configs/' + str(id), data=json.dumps(new_data), content_type='application/json').status_code == 200
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
    
def test_delete_app_config(client, app):
    """Test DELETE API"""
    id = None
    with app.app_context():
        db = conn.get_db()
        config = db[current_app.config['APP_CONFIGS_COLLECTION']].find_one({'mobileAppVersion': '0.1.0'})
        id = config['_id']
    if id is not None:
        resp = client.delete('/app/configs/' + str(id))
        assert(resp.status_code == 202)
    
    
def test_get_by_version(client, app):
    """Test POST API"""
    req_data_1 = {
        "mobileAppVersion": "0.1.0",
        "platformBuildingBlocks": {"appconfig": "https://api.rokwire.illinois.edu/app/configs"},
        "thirdPartyServices": {},
        "otherUniversityServices": {}
    }
    assert client.post('/app/configs', data=json.dumps(req_data_1), content_type='application/json').status_code == 201
    req_data_2 = {
        "mobileAppVersion": "0.2.0",
        "platformBuildingBlocks": {"events": "http://api.rokwire.illinois.edu/events"},
        "thirdPartyServices": {},
        "otherUniversityServices": {}
    }
    assert client.post('/app/configs', data=json.dumps(req_data_2), content_type='application/json').status_code == 201
    assert client.get('/app/configs?mobileAppVersion=0.2.0').status_code == 200
    response = client.get('/app/configs')
    assert b'0.1.0' in response.data
    assert b'0.2.0' in response.data
    with app.app_context():
        db = conn.get_db()
        ack = db[current_app.config['APP_CONFIGS_COLLECTION']].delete_many({'mobileAppVersion': {'$in': ['0.1.0', '0.2.0']}})