import json
from flask import current_app

from test_app_config import app, client
from appconfig import db as conn

def test_post_dup_version(client, app):
    """POST couple of app config with same mobile app version and expect error"""
    req_data_1 = {
        "mobileAppVersion": "0.1.0",
        "platformBuildingBlocks": {"appconfig": "https://api.rokwire.illinois.edu/app/configs"},
        "thirdPartyServices": {},
        "otherUniversityServices": {},
        "secretKeys": {}
    }
    assert client.post('/app/configs', data=json.dumps(req_data_1), content_type='application/json').status_code == 201
    req_data_2 = {
        "mobileAppVersion": "0.1.0",
        "platformBuildingBlocks": {"events": "http://api.rokwire.illinois.edu/events"},
        "thirdPartyServices": {},
        "otherUniversityServices": {},
        "secretKeys": {}
    }
    assert client.post('/app/configs', data=json.dumps(req_data_2), content_type='application/json').status_code == 500
    with app.app_context():
        db = conn.get_db()
        ack = db[current_app.config['APP_CONFIGS_COLLECTION']].delete_many({'mobileAppVersion': {'$in': ['0.1.0']}})