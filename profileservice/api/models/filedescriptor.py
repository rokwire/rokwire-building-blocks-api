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

class FileDescriptor:
    id = None
    deleted = None
    filename = None
    mimeType = None
    size = None
    dataURL = None
    md5sum = None

    def __init__(self):
        id = None

    def set_id(self, id):
        self.id = id

    def get_id(self):
        return self.id

    def set_deleted(self, deleted):
        self.deleted = deleted

    def get_deleted(self):
        return self.deleted

    def set_filename(self, filename):
        self.filename = filename

    def get_filename(self):
        return self.filename

    def set_mime_type(self, mime_type):
        self.mimeType = mime_type

    def get_mime_type(self):
        return self.mimeType

    def set_size(self, size):
        self.size = size

    def get_size(self):
        return self.size

    def set_data_url(self, data_url):
        self.dataURL = data_url

    def get_data_url(self):
        return self.dataURL

    def set_md5sum(self, md5sum):
        self.md5sum = md5sum

    def get_md5sum(self):
        return self.md5sum