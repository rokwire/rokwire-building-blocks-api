import json

from flask import current_app

from ..utils import db as conn


def test_post_dup_version(client, app):
    """POST couple of api config with same mobile api version and expect error"""
    req_data_1 = {
        "mobileAppVersion": "0.1.0",
        "platformBuildingBlocks": {"appconfig": "https://api.rokwire.illinois.edu/app/configs"},
        "thirdPartyServices": {},
        "otherUniversityServices": {},
        "secretKeys": "blabla",
        "upgrade": {}
    }
    assert client.post('/app/configs', data=json.dumps(req_data_1), content_type='application/json').status_code == 201
    req_data_2 = {
        "mobileAppVersion": "0.1.0",
        "platformBuildingBlocks": {"events": "http://api.rokwire.illinois.edu/events"},
        "thirdPartyServices": {},
        "otherUniversityServices": {},
        "secretKeys": "",
        "upgrade": {}
    }
    assert client.post('/app/configs', data=json.dumps(req_data_2), content_type='application/json').status_code == 500
    with app.app_context():
        db = conn.get_db()
        ack = db[current_app.config['APP_CONFIGS_COLLECTION']].delete_many({'mobileAppVersion': {'$in': ['0.1.0']}})


def test_order_by_version(client, app):
    """POST multiple api config and check order"""
    req_data_1 = {
        "mobileAppVersion": "0.9.9",
        "platformBuildingBlocks": {"appconfig": "https://api.rokwire.illinois.edu/app/configs"},
        "thirdPartyServices": {},
        "otherUniversityServices": {},
        "secretKeys": "",
        "upgrade": {}
    }
    assert client.post('/app/configs', data=json.dumps(req_data_1), content_type='application/json').status_code == 201
    req_data_2 = {
        "mobileAppVersion": "0.9.7",
        "platformBuildingBlocks": {"appconfig": "https://api.rokwire.illinois.edu/app/configs"},
        "thirdPartyServices": {},
        "otherUniversityServices": {},
        "secretKeys": "abc",
        "upgrade": {}
    }
    assert client.post('/app/configs', data=json.dumps(req_data_2), content_type='application/json').status_code == 201
    req_data_3 = {
        "mobileAppVersion": "0.9.1",
        "platformBuildingBlocks": {"appconfig": "https://api.rokwire.illinois.edu/app/configs"},
        "thirdPartyServices": {},
        "otherUniversityServices": {},
        "secretKeys": "abc",
        "upgrade": {}
    }
    assert client.post('/app/configs', data=json.dumps(req_data_3), content_type='application/json').status_code == 201
    req_data_4 = {
        "mobileAppVersion": "0.8.5",
        "platformBuildingBlocks": {"appconfig": "https://api.rokwire.illinois.edu/app/configs"},
        "thirdPartyServices": {},
        "otherUniversityServices": {},
        "secretKeys": "abc",
        "upgrade": {}
    }
    assert client.post('/app/configs', data=json.dumps(req_data_4), content_type='application/json').status_code == 201
    req_data_5 = {
        "mobileAppVersion": "0.8.1",
        "platformBuildingBlocks": {"appconfig": "https://api.rokwire.illinois.edu/app/configs"},
        "thirdPartyServices": {},
        "otherUniversityServices": {},
        "secretKeys": "abc",
        "upgrade": {}
    }
    assert client.post('/app/configs', data=json.dumps(req_data_5), content_type='application/json').status_code == 201
    req_data_6 = {
        "mobileAppVersion": "0.7.4",
        "platformBuildingBlocks": {"appconfig": "https://api.rokwire.illinois.edu/app/configs"},
        "thirdPartyServices": {},
        "otherUniversityServices": {},
        "secretKeys": "abc",
        "upgrade": {}
    }
    assert client.post('/app/configs', data=json.dumps(req_data_6), content_type='application/json').status_code == 201
    req_data_7 = {
        "mobileAppVersion": "0.7.3",
        "platformBuildingBlocks": {"appconfig": "https://api.rokwire.illinois.edu/app/configs"},
        "thirdPartyServices": {},
        "otherUniversityServices": {},
        "secretKeys": "abc",
        "upgrade": {}
    }
    assert client.post('/app/configs', data=json.dumps(req_data_7), content_type='application/json').status_code == 201
    req_data_8 = {
        "mobileAppVersion": "0.7.2",
        "platformBuildingBlocks": {"appconfig": "https://api.rokwire.illinois.edu/app/configs"},
        "thirdPartyServices": {},
        "otherUniversityServices": {},
        "secretKeys": "abc",
        "upgrade": {}
    }
    assert client.post('/app/configs', data=json.dumps(req_data_8), content_type='application/json').status_code == 201
    req_data_9 = {
        "mobileAppVersion": "0.10.11",
        "platformBuildingBlocks": {"appconfig": "https://api.rokwire.illinois.edu/app/configs"},
        "thirdPartyServices": {},
        "otherUniversityServices": {},
        "secretKeys": "abc",
        "upgrade": {}
    }
    assert client.post('/app/configs', data=json.dumps(req_data_9), content_type='application/json').status_code == 201
    response = client.get('/app/configs')
    documents = json.loads(response.data)
    size = len(documents)
    assert size == 9
    versions = []
    for doc in documents:
        v = doc['mobileAppVersion']
        versions.append(v)
    assert versions[8] == "0.7.2"
    assert versions[7] == "0.7.3"
    assert versions[6] == "0.7.4"
    assert versions[5] == "0.8.1"
    assert versions[4] == "0.8.5"
    assert versions[3] == "0.9.1"
    assert versions[2] == "0.9.7"
    assert versions[1] == "0.9.9"
    assert versions[0] == "0.10.11"
    with app.app_context():
        db = conn.get_db()
        ack = db[current_app.config['APP_CONFIGS_COLLECTION']].delete_many({'mobileAppVersion': {
            '$in': ["0.9.9", "0.9.7", "0.9.1", "0.8.5", "0.8.1", "0.7.4", "0.7.3", "0.7.2", "0.10.11"]}})
