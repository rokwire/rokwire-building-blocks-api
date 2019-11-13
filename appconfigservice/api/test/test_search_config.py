import json

from appconfig import db as conn
from flask import current_app


def test_get_by_version(client, app):
    """POST couple of api config, then search by version, finally delete those posted items."""
    req_data_1 = {
        "mobileAppVersion": "0.1.0",
        "platformBuildingBlocks": {"appconfig": "https://api.rokwire.illinois.edu/app/configs"},
        "thirdPartyServices": {},
        "otherUniversityServices": {},
        "secretKeys": {}
    }
    assert client.post('/api/configs', data=json.dumps(req_data_1), content_type='application/json').status_code == 201
    req_data_2 = {
        "mobileAppVersion": "0.2.0",
        "platformBuildingBlocks": {"events": "http://api.rokwire.illinois.edu/events"},
        "thirdPartyServices": {},
        "otherUniversityServices": {},
        "secretKeys": {}
    }
    assert client.post('/api/configs', data=json.dumps(req_data_2), content_type='application/json').status_code == 201
    assert client.get('/api/configs?mobileAppVersion=0.2.0').status_code == 200
    response = client.get('/api/configs?mobileAppVersion=0.2.0')
    assert b'0.2.0' in response.data
    documents = json.loads(response.data)
    size = len(documents)
    assert size == 1
    with app.app_context():
        db = conn.get_db()
        ack = db[current_app.config['APP_CONFIGS_COLLECTION']].delete_many(
            {'mobileAppVersion': {'$in': ['0.1.0', '0.2.0']}})


def test_search_by_bad_version(client, app):
    assert client.get('/api/configs?mobileAppVersion=0.2').status_code == 404


def test_search_by_version(client, app):
    """POST multiple api config and check order"""
    req_data_4 = {
        "mobileAppVersion": "0.9.9",
        "platformBuildingBlocks": {"appconfig": "https://api.rokwire.illinois.edu/app/configs"},
        "thirdPartyServices": {},
        "otherUniversityServices": {},
        "secretKeys": {}
    }
    assert client.post('/api/configs', data=json.dumps(req_data_4), content_type='application/json').status_code == 201
    req_data_1 = {
        "mobileAppVersion": "0.9.7",
        "platformBuildingBlocks": {"appconfig": "https://api.rokwire.illinois.edu/app/configs"},
        "thirdPartyServices": {},
        "otherUniversityServices": {},
        "secretKeys": {}
    }
    assert client.post('/api/configs', data=json.dumps(req_data_1), content_type='application/json').status_code == 201
    req_data_2 = {
        "mobileAppVersion": "0.8.5",
        "platformBuildingBlocks": {"appconfig": "https://api.rokwire.illinois.edu/app/configs"},
        "thirdPartyServices": {},
        "otherUniversityServices": {},
        "secretKeys": {}
    }
    assert client.post('/api/configs', data=json.dumps(req_data_2), content_type='application/json').status_code == 201
    req_data_3 = {
        "mobileAppVersion": "0.10.11",
        "platformBuildingBlocks": {"appconfig": "https://api.rokwire.illinois.edu/app/configs"},
        "thirdPartyServices": {},
        "otherUniversityServices": {},
        "secretKeys": {}
    }
    assert client.post('/api/configs', data=json.dumps(req_data_3), content_type='application/json').status_code == 201
    req_data_5 = {
        "mobileAppVersion": "10.1.11",
        "platformBuildingBlocks": {"appconfig": "https://api.rokwire.illinois.edu/app/configs"},
        "thirdPartyServices": {},
        "otherUniversityServices": {},
        "secretKeys": {}
    }
    assert client.post('/api/configs', data=json.dumps(req_data_5), content_type='application/json').status_code == 201
    req_data_6 = {
        "mobileAppVersion": "5.9.10",
        "platformBuildingBlocks": {"appconfig": "https://api.rokwire.illinois.edu/app/configs"},
        "thirdPartyServices": {},
        "otherUniversityServices": {},
        "secretKeys": {}
    }
    assert client.post('/api/configs', data=json.dumps(req_data_6), content_type='application/json').status_code == 201
    req_data_7 = {
        "mobileAppVersion": "0.7.2",
        "platformBuildingBlocks": {"appconfig": "https://api.rokwire.illinois.edu/app/configs"},
        "thirdPartyServices": {},
        "otherUniversityServices": {},
        "secretKeys": {}
    }
    assert client.post('/api/configs', data=json.dumps(req_data_7), content_type='application/json').status_code == 201
    response = client.get('/api/configs?mobileAppVersion=10.0.0')
    documents = json.loads(response.data)
    versions = []
    for doc in documents:
        versions.append(doc['mobileAppVersion'])
    assert len(versions) == 1
    assert versions[0] == "5.9.10"
    with app.app_context():
        db = conn.get_db()
        ack = db[current_app.config['APP_CONFIGS_COLLECTION']].delete_many(
            {'mobileAppVersion': {'$in': ["0.9.9", "0.9.7", "0.8.5", "0.10.11", "10.1.11", "5.9.10", "0.7.2"]}})
