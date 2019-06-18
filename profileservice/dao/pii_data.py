import profileservice.restservice.utils.datasetutils as datasetutils

class PiiData():
    def __init__(self, injson):
        self.lastname = None
        self.firstname = None
        self.phone = None
        self.email = None
        self.username = None
        self.uin = None
        self.netid = None
        self.pid = None
        self.uuid = None
        self.imageUrl = None
        self.fileDescriptors = None
        self.creationDate = None
        self.lastModifiedDate = None

        self = datasetutils.update_pii_dataset_from_json(self, injson)

    def set_pid(self, pid):
        self.pid = pid

    def get_pid(self):
        return self.pid

    def set_lastname(self, lastname):
        self.lastname = lastname

    def get_lastname(self):
        return self.lastname

    def set_firstname(self, firstname):
        self.firstname = firstname

    def get_firstname(self):
        return self.firstname

    def set_phone(self, phone):
        self.phone = phone

    def get_phone(self):
        return self.phone

    def set_email(self, email):
        self.email = email

    def get_email(self):
        return self.email

    def set_username(self, username):
        self.username = username

    def get_username(self):
        return self.username

    def set_uin(self, uin):
        self.uin = uin

    def get_uin(self):
        return self.uin

    def set_netid(self, netid):
        self.netid = netid

    def get_netid(self):
        return self.netid

    def add_uuid(self, uuid):
        if (uuid != None):
            self.get_uuid().append(uuid)

    def set_uuid(self, uuid):
        self.uuid = uuid

    def get_uuid(self):
        return self.uuid

    def add_file_descriptor(self, fileDescriptor):
        if (fileDescriptor is not None):
            self.get_file_descriptors().append(fileDescriptor)

    def set_file_descriptors(self, fileDescriptors):
        self.fileDescriptors = fileDescriptors

    def get_file_descriptors(self):
        return self.fileDescriptors

    def set_image_url(self, imageUrl):
        self.imageUrl = imageUrl

    def get_image_url(self):
        return self.imageUrl

    def set_creation_date(self, creationDate):
        self.creationDate = creationDate

    def get_creation_date(self):
        return self.creationDate

    def set_last_modified_date(self, lastModifiedDate):
        self.lastModifiedDate = lastModifiedDate

    def get_last_modified_date(self):
        return self.lastModifiedDate