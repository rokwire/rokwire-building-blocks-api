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

class SelfCertification:
    def __init__(self):
        self.dataDeletionUponRequest = None
        self.respectingUserPrivacySetting = None
        self.discloseAds = None
        self.discloseSponsors = None
        self.discloseImageRights = None

    def set_data_deletion_upon_request(self, dataDeletionUponRequest):
        self.dataDeletionUponRequest = dataDeletionUponRequest

    def get_data_deletion_upon_request(self):
        return self.dataDeletionUponRequest

    def set_respecting_user_privacy_setting(self, respectingUserPrivacySetting):
        self.respectingUserPrivacySetting = respectingUserPrivacySetting

    def get_respecting_user_privacy_setting(self):
        return self.respectingUserPrivacySetting

    def set_disclose_ads(self, discloseAds):
        self.discloseAds = discloseAds

    def get_disclose_ads(self):
        return self.discloseAds

    def set_disclose_sponsors(self, discloseSponsors):
        self.discloseSponsors = discloseSponsors

    def get_disclose_sponsors(self):
        return self.discloseSponsors

    def set_disclose_image_rights(self, discloseImageRights):
        self.discloseImageRights = discloseImageRights

    def get_disclose_image_rights(self):
        return self.discloseImageRights
