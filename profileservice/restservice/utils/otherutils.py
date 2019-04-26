import hashlib
import os
import urllib
from mimetypes import MimeTypes

from bson import ObjectId

from profileservice.dao.filedescriptor import FileDescriptor

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