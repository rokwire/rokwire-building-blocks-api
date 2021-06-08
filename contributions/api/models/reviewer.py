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

import contributions.api.utils.datasetutils as datasetutils

class Reviewer:
    def __init__(self, injson):
        self.name = None
        self.githubUsername = None
        self.dateCreated = None

        self, restjson = datasetutils.update_reviwer_dataset_from_json(self, injson)

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_github_username(self, githubUsername):
        self.githubUsername = githubUsername

    def get_github_username(self):
        return self.githubUsername

    def set_date_created(self, dateCreated):
        self.dateCreated = dateCreated

    def get_date_created(self):
        return self.dateCreated
