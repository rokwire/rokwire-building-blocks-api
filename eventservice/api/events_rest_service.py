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

import connexion
import controllers.configs as cfg
from utils.db import init_db
from rokwireresolver import RokwireResolver

debug = cfg.DEBUG

init_db()

app = connexion.FlaskApp(__name__, debug=debug, specification_dir=cfg.API_LOC)
app.add_api('rokwire.yaml', base_path=cfg.URL_PREFIX, arguments={'title': 'Rokwire'}, resolver=RokwireResolver('controllers'),
            resolver_error=501)

if __name__ == '__main__':
    app.run(port=5000, host=None, server='flask', debug=debug)
