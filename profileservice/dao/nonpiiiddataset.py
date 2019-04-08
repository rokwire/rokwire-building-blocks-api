"""
author: Yong Wook Kim
created 2019 Apr 4
"""
import uuid

class NonPiiidDataset:
    def __init__(self):
        self.non_pii_uuid = None
        self.id = None
        self.hobby = None
        self.set_non_pii_uuid(str(uuid.uuid4()))

    def get_non_pii_uuid(self):
        return self.non_pii_uuid

    def set_non_pii_uuid(self, non_pii_uuid):
        self.non_pii_uuid = non_pii_uuid

    def add_non_pii_id(self, non_pii_id):
        if (non_pii_id != None):
            self.get_non_pii_id().append(non_pii_id)

    def set_id(self, id):
        self.id = id

    def get_id(self):
        return self.id

    def set_hobby(self, hobby):
        self.hobby = hobby

    def get_hobby(self):
        return self.hobby

    def add_hobby(self, hobby):
        if (hobby != None):
            self.get_hobby().append(hobby)