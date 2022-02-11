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

class Review:
    def __init__(self, injson):
        self.reviewerId = None
        self.reviewComment = None
        self.reviewLastUpdated = None

        self, restjson = datasetutils.update_review_dataset_from_json(self, injson)

    def set_reviewer_id(self, reviewerId):
        self.reviewerId = reviewerId

    def get_reviewer_id(self):
        return self.reviewerId

    def set_review_comment(self, reviewComment):
        self.reviewComment = reviewComment

    def get_review_comment(self):
        return self.reviewComment

    def set_review_last_updated(self, reviewLastUpdated):
        self.reviewLastUpdated = reviewLastUpdated

    def get_review_last_updated(self):
        return self.reviewLastUpdated
