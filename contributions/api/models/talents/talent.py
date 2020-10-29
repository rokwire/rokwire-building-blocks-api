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

import utils.datasetutils as datasetutils

class Talent():
    def __init__(self, injson):
        self.name = None
        self.shortDescription = None
        self.longDescription = None
        self.requiredCapabilities = None
        self.requiredBuildingBlocks = None
        self.minUserPrivacyLevel = None
        self.minEndUserRoles = None
        self.startDate = None
        self.endDate = None
        self.dataDescription = None
        self.selfCertification = None

        self, restjson = datasetutils.update_talent_dataset_from_json(self, injson)

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_short_description(self, shortDescription):
        self.shortDescription = shortDescription

    def get_short_description(self):
        return self.shortDescription

    def set_long_description(self, longDescription):
        self.longDescription = longDescription

    def get_long_description(self):
        return self.longDescription

    def set_required_capabilities(self, requiredCapabilities):
        self.requiredCapabilities = requiredCapabilities

    def get_required_capabilities(self):
        return self.requiredCapabilities

    def set_required_building_blocks(self, requiredBuildingBlocks):
        self.requiredBuildingBlocks = requiredBuildingBlocks

    def get_required_building_blocks(self):
        return self.requiredBuildingBlocks

    def set_min_user_privacy_level(self, minUserPrivacyLevel):
        self.minUserPrivacyLevel = minUserPrivacyLevel

    def get_min_user_privacy_level(self):
        return self.minUserPrivacyLevel

    def set_min_end_user_roles(self, minEndUserRoles):
        self.minEndUserRoles = minEndUserRoles

    def get_min_end_user_roles(self):
        return self.minEndUserRoles

    def set_start_date(self, startDate):
        self.startDate = startDate

    def get_start_date(self):
        return self.startDate

    def set_end_date(self, endDate):
        self.endDate = endDate

    def get_end_date(self):
        return self.endDate

    def set_data_description(self, dataDescription):
        self.dataDescription = dataDescription

    def get_data_description(self):
        return self.dataDescription

    def set_self_certification(self, selfCertification):
        self.selfCertification = selfCertification

    def get_self_certification(self):
        return self.selfCertification
