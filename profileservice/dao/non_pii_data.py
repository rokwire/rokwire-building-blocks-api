import uuid as uuidlib
import profileservice.restservice.utils.datasetutils as datasetutils

class non_pii_data:
    def __init__(self, injson):
        self.uuid = None
        self.generalInterests = None
        self.athleticsInterests = None
        self.fileDescriptors = None
        self.imageUrl = None
        self.over13 = None
        self.creationDate = None
        self.lastModifiedDate = None

        self = datasetutils.update_non_pii_dataset_from_json(self, injson)

    def set_uuid(self, uuid):
        self.uuid = uuid

    def get_uuid(self):
        return self.uuid

    def set_over13(self, over13):
        self.over13 = over13

    def get_over13(self):
        return self.over13

    def set_general_interests(self, generalInterests):
        self.generalInterests = generalInterests

    def get_general_interests(self):
        return self.generalInterests

    def add_general_interest(self, generalInterest):
        if (generalInterest is not None):
            self.get_general_interests().append(generalInterest)

    def set_athletics_interests(self, athleticsInterests):
        self.athleticsInterests = athleticsInterests

    def get_athletics_interests(self):
        return self.athleticsInterests

    def add_athletics_interest(self, athleticsInterest):
        if (athleticsInterest is not None):
            self.get_athletics_interests().append(athleticsInterest)

    def add_file_descriptor(self, fileDescriptor):
        if (fileDescriptor is not None):
            self.get_file_descriptors().append(fileDescriptor)

    def set_file_descriptors(self, fileDescriptors):
        self.fileDescriptors = fileDescriptors

    def get_file_descriptors(self):
        return self.fileDescriptors

    def set_image_uri(self, image_uri):
        self.imageUrl = image_uri

    def get_image_uri(self):
        return self.imageUrl

    def set_creation_date(self, creationDate):
        self.creationDate = creationDate

    def get_creation_date(self):
        return self.creationDate

    def set_last_modified_date(self, lastModifiedDate):
        self.lastModifiedDate = lastModifiedDate

    def get_last_modified_date(self):
        return self.lastModifiedDate

