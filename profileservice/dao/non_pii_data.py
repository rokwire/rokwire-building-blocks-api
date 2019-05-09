import uuid as uuidlib
import profileservice.restservice.utils.datasetutils as datasetutils

class non_pii_data:
    def __init__(self, injson):
        self.uuid = None
        self.general_interests = None
        self.athletics_interests = None
        self.file_descriptors = None
        self.image_uri = None
        self.over13 = None
        self.first_modified_date = None
        self.last_modified_date = None

        self = datasetutils.update_non_pii_dataset_from_json(self, injson)

    def set_uuid(self, uuid):
        self.uuid = uuid

    def get_uuid(self):
        return self.uuid

    def set_over13(self, over13):
        self.over13 = over13

    def get_over13(self):
        return self.over13

    def set_general_interests(self, general_interests):
        self.general_interests = general_interests

    def get_general_interests(self):
        return self.general_interests

    def add_general_interests(self, general_interests):
        if (general_interests is not None):
            self.get_general_interests().append(general_interests)
    def set_athletics_interests(self, athletics_interests):
        self.athletics_interests = athletics_interests

    def get_athletics_interests(self):
        return self.athletics_interests

    def add_athletics_interests(self, athletics_interests):
        if (athletics_interests is not None):
            self.get_athletics_interests().append(athletics_interests)

    def add_file_descriptor(self, file_descriptor):
        if (file_descriptor is not None):
            self.get_file_descriptors().append(file_descriptor)

    def set_file_descriptors(self, file_descriptors):
        self.file_descriptors = file_descriptors

    def get_file_descriptors(self):
        return self.file_descriptors

    def set_image_uri(self, image_uri):
        self.image_uri = image_uri

    def get_image_uri(self):
        return self.image_uri

    def set_first_modified_date(self, first_modified_date):
        self.first_modified_date = first_modified_date

    def get_first_modified_date(self):
        return self.first_modified_date

    def set_last_modified_date(self, last_modified_date):
        self.last_modified_date = last_modified_date

    def get_last_modified_date(self):
        return self.last_modified_date

