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

import flask
import auth_middleware
from dotenv import load_dotenv

# Load .env file
load_dotenv()

app = flask.Flask(__name__)


################################################
# Call middleware here!
################################################
app.before_request(auth_middleware.authenticate)


@app.route('/')
def hello_world():
    return "Hello world!"

@app.route('/authorize')
def authorize():
    id_info = auth_middleware.authenticate()
    group_list = None
    try:
        group_list = id_info["uiucedu_is_member_of"]
    except Exception:
        raise Exception('Token did not contain the group info')
    auth_middleware.authorize(group_list)
    auth_middleware.authorize(auth_middleware.rokwire_app_config_manager_group)
    return "authorized"

if __name__ == '__main__':
    app.run(port=5000, debug=True)
