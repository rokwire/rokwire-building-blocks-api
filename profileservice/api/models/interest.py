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

class Interest():
    def __init__(self):
        self.category = None
        self.subcategories = None

    def set_category(self, category):
        self.category = category

    def get_category(self):
        return self.category

    def add_subcategories(self, subcategory):
        if (subcategory is not None):
            self.get_subcategories().append(subcategory)

    def set_subcategories(self, subcategories):
        self.subcategories = subcategories

    def get_subcategories(self):
        return self.subcategories