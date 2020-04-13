from flask import make_response

def remove_objectid_from_dataset(dataset):
    if "_id" in dataset:
        del dataset["_id"]

    return dataset

def create_log_json(ep_name, ep_method, in_json):
    in_json['ep_building_block'] = "capability_building_block"
    in_json['ep_name'] = ep_name
    in_json['ep_method'] = ep_method

    return in_json

def create_auth_fail_message():
    out_json = make_response("{\"Authorization Failed\": \"The user info in id token and db are not matching.\"}")
    out_json.mimetype = 'application/json'
    out_json.status_code = 403

    return out_json