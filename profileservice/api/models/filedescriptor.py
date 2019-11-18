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