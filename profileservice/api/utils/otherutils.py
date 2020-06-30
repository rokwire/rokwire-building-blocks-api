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

import hashlib
import os
import urllib

from datetime import datetime
from mimetypes import MimeTypes

from bson import ObjectId

from models.filedescriptor import FileDescriptor

"""
create FileDescriptor object
"""
def create_file_descriptor(data_repo_dir, file):
    filename = file.filename
    fd = FileDescriptor()
    new_id = ObjectId()
    new_id = str(new_id)
    fd.set_id(new_id)

    # create folder
    levels = 2
    path = ''
    i = 0
    while (i < levels * 2 and len(new_id) >= i + 2):
        path = path + new_id[i: i + 2] + os.sep
        i = i + 2

    if (len(new_id) > 0):
        path = path + new_id + os.sep

    path = data_repo_dir + os.sep + path

    if not os.path.exists(path):
        os.makedirs(path)

    # save file to path
    file.save(os.path.join(path, filename))

    # if os.path.isfile(filename):
    #     shutil.copy(filename, path)

    saved_file = path + os.path.basename(filename)
    fd.set_data_url('file:' + os.sep + saved_file)

    fd.set_filename(os.path.basename(filename))

    mime = MimeTypes()
    mime_type = mime.guess_type(urllib.request.pathname2url(filename))
    if mime_type[0] == None:
        fd.set_mime_type('application/octet-stream')
    else:
        fd.set_mime_type(mime_type[0])

    file_stat = os.stat(saved_file)
    fd.set_size(file_stat.st_size)

    hash_md5 = hashlib.md5()
    with open(saved_file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    fd.set_md5sum(hash_md5.hexdigest())

    return fd

"""
convert utd time format for rokwire
"""
def get_current_time_utc():
    currenttime = datetime.utcnow()
    formattedtime, micro = currenttime.strftime('%Y-%m-%dT%H:%M:%S.%f').split('.')
    formattedtime = "%s.%03dZ" % (formattedtime, int(micro) / 1000)

    return formattedtime

"""
check privacy level to see if they are correct value
"""
def check_privacy_level(in_json):
    level_str = ["1", "2", "3", "4", "5"]
    level_ok = False
    try:
        level = in_json["privacySettings"]["level"]
        for i in range(len(level_str)):
            if str(level) == level_str[i]:
                level_ok = True
        return level_ok, str(level)
    except:
        return True, ""