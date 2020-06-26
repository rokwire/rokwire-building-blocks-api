#  Copyright (c) 2020 by the Board of Trustees of the University of Illinois
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
        self.firstname = None
        self.middlename = None
        self.lastname = None
        self.email = None
        self.phone = None
        self.affiliation = None

        self, restjson = datasetutils.update_person_dataset_from_json(self, injson)

    def set_firstname(self, firstname):
        self.firstname = firstname

    def get_firstname(self):
        return self.firstname

    def set_middlename(self, middlename):
        self.middlename = middlename

    def get_middlename(self):
        return self.middlename

    def set_lastname(self, lastname):
        self.lastname = lastname

    def get_lastname(self):
        return self.lastname

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