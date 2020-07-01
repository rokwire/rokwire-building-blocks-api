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

class TestResultsConsent():
    def __init__(self):
        self.consentProvided  = None
        self.dateModified   = None

    def set_consent_provided(self, consentProvided ):
        self.consentProvided  = consentProvided

    def get_consent_provided(self):
        return self.consentProvided

    def set_date_modified(self, dateModified ):
        self.dateModified  = dateModified

    def get_date_modified(self):
        return self.dateModified