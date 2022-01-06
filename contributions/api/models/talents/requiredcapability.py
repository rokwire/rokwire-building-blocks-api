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

class RequiredCapability:
    def __init__(self):
        self.contributionId = None
        self.capabilityId = None
        self.capabilityName = None

    def set_contribution_id(self, contributionId):
        self.contributionId = contributionId

    def get_contribution_id(self):
        return self.contributionId

    def set_capability_id(self, capabilityId):
        self.capabilityId = capabilityId

    def get_capability_id(self):
        return self.capabilityId

    def set_capability_name(self, capabilityName):
        self.capabilityName = capabilityName

    def get_capability_name(self):
        return self.capabilityName
