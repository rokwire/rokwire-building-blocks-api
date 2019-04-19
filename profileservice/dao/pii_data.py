"""
author: Yong Wook Kim
created 2019 Apr 4
"""
import uuid

class pii_data:
    def __init__(self):
        self.objectid = None
        self.lastname = None
        self.firstname = None
        self.phonenumber = None
        self.email = None
        self.netid = None
        self.uin = None
        self.pii_uuid = None
        self.set_pii_uuid(str(uuid.uuid4()))

    def set_pii_uuid(self, pii_uuid):
        self.pii_uuid = pii_uuid

    def get_pii_uuid(self):
        return self.pii_uuid

    def add_pii_uuid(self, pii_uuid):
        if (pii_uuid != None):
            self.get_pii_uuid().append(pii_uuid)

    def set_objectid(self, objectid):
        self.objectid = objectid

    def get_objectid(self):
        return self.objectid

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

    def set_netid(self, netid):
        self.netid = netid

    def get_netid(self):
        return self.netid

    def set_uin(self, uin):
        self.uin = uin

    def get_uin(self):
        return self.uin