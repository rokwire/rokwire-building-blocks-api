#  Copyright 2021 Board of Trustees of the University of Illinois.
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

from flask import make_response


def create_log_json(ep_name, ep_method, in_json):
    """
    create a json for logging
    """
    out_json = {}
    out_json['ep_building_block'] = "events_building_block"
    out_json['ep_name'] = ep_name
    out_json['ep_method'] = ep_method
    if 'tags' in in_json:
        out_json['tags'] = in_json['tags']
    if 'title' in in_json:
        out_json['title'] = in_json['title']
    if 'description' in in_json:
        out_json['longDescription'] = in_json['description']
    elif 'longDescription' in in_json:
        out_json['longDescription'] = in_json['longDescription']
    if len(in_json) == 0:
        out_json['ep_method_status'] = "failed"
    else:
        out_json['ep_method_status'] = "success"

    return out_json
