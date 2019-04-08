"""
author: Yong Wook Kim
created 2019 Apr 4
"""
import uuid

class PiiidDataset:
    def __init__(self):
        self.id = None
        self.lastname = None
        self.firstname = None
        self.phonenumber = None
        self.email = None
        self.userid = None
        self.pii_uuid = None
        self.set_pii_uuid(str(uuid.uuid4()))

    def set_pii_uuid(self, pii_uuid):
        self.pii_uuid = pii_uuid

    def get_pii_uuid(self):
        return self.pii_uuid

    def add_pii_id(self, pii_id):
        if (pii_id != None):
            self.get_pii_id().append(pii_id)

    def set_id(self, id):
        self.id = id

    def get_id(self):
        return self.id

    def set_lastname(self, lastname):
        self.lastname = lastname

    def get_lastname(self):
        return self.lastname

    def set_firstname(self, firstname):
        self.firstname = firstname

    def get_firstname(self):
        return self.firstname

    def set_phonenumber(self, phonenumber):
        self.phonenumber = phonenumber

    def get_phonenumber(self):
        return self.phonenumber

    def set_email(self, email):
        self.email = email

    def get_email(self):
        return self.email

    def set_userid(self, userid):
        self.userid = userid

    def get_userid(self):
        return self.userid