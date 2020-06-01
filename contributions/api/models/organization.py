import utils.datasetutils as datasetutils

class Organization:
    def __init__(self, injson):
        self.name = None
        self.address = None
        self.email = None
        self.phone = None

        self, restjson = datasetutils.update_organization_dataset_from_json(self, injson)

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_address(self, address):
        self.address = address

    def get_address(self):
        return self.address

    def set_email(self, email):
        self.email = email

    def get_email(self):
        return self.email

    def set_phone(self, phone):
        self.phone = phone

    def get_phone(self):
        return self.phone