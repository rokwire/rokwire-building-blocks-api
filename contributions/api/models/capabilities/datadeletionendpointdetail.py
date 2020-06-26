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

class DataDeletionEndpointDetail:
    def __init__(self):
        self.deletionEndpoint = None
        self.description = None
        self.apiKey = None

    def set_deletion_endpoint(self, deletionEndpoint):
        self.deletionEndpoint = deletionEndpoint

    def get_deletion_endpoint(self):
        return self.deletionEndpoint

    def set_description(self, description):
        self.description = description

    def get_description(self):
        return self.description

    def set_api_key(self, apiKey):
        self.apiKey = apiKey

    def get_api_key(self):
        return self.apiKey
