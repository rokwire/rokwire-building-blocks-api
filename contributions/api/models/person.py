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

class Person:
    def __init__(self, injson):
        self.contributorType = None
        self.firstName = None
        self.middleName = None
        self.lastName = None
        self.email = None
        self.phone = None
        self.affiliation = None

        self, restjson = datasetutils.update_person_dataset_from_json(self, injson)

    def set_contributor_type(self, contributorType):
        self.contributorType = contributorType

    def get_contributor_type(self):
        return self.contributorType

    def set_first_name(self, firstName):
        self.firstName = firstName

    def get_first_name(self):
        return self.firstName

    def set_middle_name(self, middleName):
        self.middleName = middleName

    def get_middle_name(self):
        return self.middleName

    def set_last_name(self, lastName):
        self.lastName = lastName

    def get_last_name(self):
        return self.lastName

    def set_email(self, email):
        self.email = email

    def get_email(self):
        return self.email

    def set_phone(self, phone):
        self.phone = phone

    def get_phone(self):
        return self.phone

    def set_affiliation(self, affiliation):
        self.affiliation = affiliation

    def get_affiliation(self):
        return self.affiliation
