import uuid as uuidlib
import profileservice.restservice.utils.datasetutils as datasetutils

class non_pii_data:
    def __init__(self, injson):
        self.uuid = None
        self.interests = None
        self.interest = Interest()
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

    def add_interests(self, interest):
        if (interest is not None):
            self.get_interests().append(interest)

    def set_interests(self, interests):
        self.interests = interests

    def get_interests(self):
        return self.interests

    def set_creation_date(self, creationDate):
        self.creationDate = creationDate

    def get_creation_date(self):
        return self.creationDate

    def set_last_modified_date(self, lastModifiedDate):
        self.lastModifiedDate = lastModifiedDate

    def get_last_modified_date(self):
        return self.lastModifiedDate

class Interest():
    def __init__(self):
        self.category = None
        self.subcategories = None

    def set_category(self, category):
        self.category = category

    def get_category(self):
        return self.category

    def add_subcategories(self, subcategories):
        if (subcategories is not None):
            self.get_subcategories().append(subcategories)

    def set_subcategories(self, subcategories):
        self.subcategories = subcategories

    def get_subcategories(self):
        return self.subcategories