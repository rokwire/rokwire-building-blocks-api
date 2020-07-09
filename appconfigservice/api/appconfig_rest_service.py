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

import logging
from time import gmtime

import connexion
from controllers.config import API_LOC
from controllers.config import APP_CONFIG_URL_PREFIX
from controllers.config import DEBUG
from rokwireresolver import RokwireResolver
from utils import db

debug = DEBUG

log = logging.getLogger('werkzeug')
log.disabled = True

logging.Formatter.converter = gmtime
log_format = '%(asctime)-15s.%(msecs)03dZ %(levelname)-7s [%(threadName)-10s] : %(name)s - %(message)s'

if debug:
    logging.basicConfig(datefmt='%Y-%m-%dT%H:%M:%S', format=log_format, level=logging.DEBUG)
else:
    logging.basicConfig(datefmt='%Y-%m-%dT%H:%M:%S', format=log_format, level=logging.INFO)

db.init_db()

app = connexion.FlaskApp(__name__, specification_dir=API_LOC)
app.add_api('rokwire.yaml', base_path=APP_CONFIG_URL_PREFIX, arguments={'title': 'Rokwire'},
            resolver=RokwireResolver('controllers'),
            resolver_error=501)

if __name__ == '__main__':
    app.run(port=5000, host=None, server='flask', debug=debug)
