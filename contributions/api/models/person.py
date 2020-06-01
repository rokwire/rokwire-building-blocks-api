import utils.datasetutils as datasetutils

class Person:
    def __init__(self, injson):
        self.firstname = None
        self.middlename = None
        self.lastname = None
        self.email = None
        self.phone = None
        self.affiliation = None

        self, restjson = datasetutils.update_person_dataset_from_json(self, injson)

    def set_firstname(self, firstname):
        self.firstname = firstname

    def get_firstname(self):
        return self.firstname

    def set_middlename(self, middlename):
        self.middlename = middlename

    def get_middlename(self):
        return self.middlename

    def set_lastname(self, lastname):
        self.lastname = lastname

    def get_lastname(self):
        return self.lastname

    def set_email(self, email):
        self.email = email

    def get_email(self):
        return self.email

    def set_phone(self, phone):
        self.phone = phone

    def get_phone(self):
        return self.phone

    def set_affiliation(self, affiliation):
        self.affiliation = affiliation

    def get_affiliation(self):
        return self.affiliation