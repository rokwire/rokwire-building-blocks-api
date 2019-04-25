"""
author: Yong Wook Kim (NCSA ywkim@illinois.edu)
created 2019 Apr 4
"""
import uuid
from profileservice.dao.pii_data import pii_data
from profileservice.dao.non_pii_data import non_pii_data
from bson import ObjectId

class ProfileDataset:
    def __init__(self, injson):
        self.pii_data = None
        self.non_pii_data = None
        self.uuid = None
        self.device_id = None
        self.file_descriptors = None
        self.image_uri = None

        try:
            self.set_uuid(injson["uuid"])
        except:
            self.set_uuid(str(uuid.uuid4()))

        try:
            self.set_pii_data(injson["pii_data"])
        except:
            pass
        try:
            self.set_non_pii_data(injson["non_pii_data"])
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

    def get_pii_data(self):
        return self.pii_data

    def set_pii_data(self, pii):
        if (pii != None):
            self.pii_data = pii_data()
            try:
                self.pii_data.set_objectid(pii["id"])
            except:
                new_id = ObjectId()
                new_id = str(new_id)
                self.pii_data.set_objectid(new_id)

            try:
                self.pii_data.set_pii_uuid(pii["pii_uuid"])
            except:
                pass

            try:
                self.pii_data.set_lastname(pii['lastname'])
            except Exception as e:
                pass
            try:
                self.pii_data.set_firstname(pii['firstname'])
            except Exception as e:
                pass
            try:
                self.pii_data.set_phone(pii['phone'])
            except Exception as e:
                pass
            try:
                self.pii_data.set_email(pii['email'])
            except Exception as e:
                pass
            try:
                self.pii_data.set_netid(pii['netid'])
            except Exception as e:
                pass
            try:
                self.pii_data.set_uin(pii['uin'])
            except Exception as e:
                pass

    def get_non_pii_data(self):
        return self.non_pii_data

    def set_non_pii_data(self, non_pii):
        if (non_pii != None):
            self.non_pii_data = non_pii_data()
            try:
                self.non_pii_data.set_objectid(non_pii["id"])
            except:
                new_id = ObjectId()
                new_id = str(new_id)
                self.non_pii_data.set_objectid(new_id)
            try:
                self.non_pii_data.set_general_interests(non_pii["general_interests"])
            except Exception as e:
                pass
            try:
                self.non_pii_data.set_athletics_interests(non_pii["athletics_interests"])
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