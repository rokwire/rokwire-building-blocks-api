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

import os
import shutil
import tempfile
import controllers.configs as cfg


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in cfg.ALLOWED_EXTENSIONS


def savefile(file, filename):
    try:
        _, tmpfolder = os.path.split(tempfile.mkdtemp())
        tmpfolder = cfg.IMAGE_FILE_MOUNTPOINT + tmpfolder
        os.mkdir(tmpfolder)
        tmpfile = tmpfolder + "/" + filename
        file.save(tmpfile)
    except Exception as ex:
        raise
    return tmpfile


def deletefile(tmpfile):
    try:
        if os.path.exists(tmpfile):
            tmpfolder, _ = os.path.split(tmpfile)
            shutil.rmtree(tmpfolder)
    except Exception as ex:
        pass
