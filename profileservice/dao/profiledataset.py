"""
author: Yong Wook Kim
created 2019 Apr 4
"""
import uuid
from profileservice.dao.piiiddataset import PiiidDataset
from profileservice.dao.nonpiiiddataset import NonPiiidDataset
from bson import ObjectId

class ProfileDataset:
    def __init__(self, injson):
        self.piiidDataset = None
        self.nonPiiidDataset = None
        self.uuid = None
        self.device_id = None
        self.username = None
        self.file_descriptors = None
        self.image_uri = None

        try:
            self.set_uuid(injson["uuid"])
        except:
            self.set_uuid(str(uuid.uuid4()))

        try:
            self.set_piiid_dataset(injson["piiidDataset"])
        except:
            pass
        try:
            self.set_non_piiid_dataset(injson["nonPiiidDataset"])
        except:
            pass
        try:
            self.set_username(injson['username'])
        except:
            pass
        try:
            self.set_device_id(injson['device_id'])
        except:
            pass
        try:
            self.set_file_descriptors(injson['file_descriptors'])
        except:
            pass
        try:
            self.set_image_uri(injson['image_uri'])
        except:
            pass

    def get_username(self):
        return self.username

    def set_username(self, username):
        self.username = username

    def get_uuid(self):
        return self.uuid

    def set_uuid(self, uuid):
        self.uuid = uuid

    def get_device_id(self):
        return self.device_id

    def set_device_id(self, device_id):
        self.device_id = device_id

    def add_device_id(self, device_id):
        if (device_id != None):
            self.get_device_id().append(device_id)

    def get_piiid_dataset(self):
        return self.piiidDataset

    def set_piiid_dataset(self, pii):
        if (pii != None):
            self.piiidDataset = PiiidDataset()
            try:
                self.piiidDataset.set_id(pii["id"])
            except:
                new_id = ObjectId()
                new_id = str(new_id)
                self.piiidDataset.set_id(new_id)

            try:
                self.piiidDataset.set_pii_uuid(pii["pii_uuid"])
            except:
                pass

            try:
                self.piiidDataset.set_lastname(pii['lastname'])
            except Exception as e:
                pass
            try:
                self.piiidDataset.set_firstname(pii['firstname'])
            except Exception as e:
                pass
            try:
                self.piiidDataset.set_phonenumber(pii['phonenumber'])
            except Exception as e:
                pass
            try:
                self.piiidDataset.set_email(pii['email'])
            except Exception as e:
                pass
            try:
                self.piiidDataset.set_userid(pii['userid'])
            except Exception as e:
                pass

    def get_non_piiid_dataset(self):
        return self.nonPiiidDataset

    def set_non_piiid_dataset(self, non_pii):
        if (non_pii != None):
            self.nonPiiidDataset = NonPiiidDataset()
            try:
                self.nonPiiidDataset.set_id(non_pii["id"])
            except:
                new_id = ObjectId()
                new_id = str(new_id)
                self.nonPiiidDataset.set_id(new_id)

            try:
                self.nonPiiidDataset.set_non_pii_uuid(non_pii["non_pii_uuid"])
            except:
                pass

            try:
                self.nonPiiidDataset.set_hobby(non_pii["hobby"])
            except Exception as e:
                pass

    def add_file_descriptor(self, file_descriptor):
        if (file_descriptor != None):
            self.get_file_descriptors().append(file_descriptor)

    def set_file_descriptors(self, file_descriptors):
        self.file_descriptors = file_descriptors

    def get_file_descriptors(self):
        return self.file_descriptors

    def set_image_uri(self, image_uri):
        self.image_uri = image_uri

    def get_image_uri(self):
        return self.image_uri