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

class Contact:
    def __init__(self):
        self.name = None
        self.email = None
        self.phone = None
        self.organization = None
        self.officialAddress = None

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_email(self, email):
        self.email = email

    def get_email(self):
        return self.email

    def set_phone(self, phone):
        self.phone = phone

    def get_phone(self):
        return self.phone

    def set_organization(self, organization):
        self.organization = organization

    def get_organization(self):
        return self.organization

    def set_officialAddress(self, officialAddress):
        self.officialAddress = officialAddress

    def get_officialAddress(self):
        return self.officialAddress
