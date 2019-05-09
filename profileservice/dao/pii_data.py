import profileservice.restservice.utils.datasetutils as datasetutils

class pii_data:
    def __init__(self, injson):
        self.lastname = None
        self.firstname = None
        self.phone = None
        self.email = None
        self.username = None
        self.uin = None
        self.pii_uuid = None
        self.uuid = None
        self.first_modified_date = None
        self.last_modified_date = None

        self = datasetutils.update_pii_dataset_from_json(self, injson)

    def set_pii_uuid(self, pii_uuid):
        self.pii_uuid = pii_uuid

    def get_pii_uuid(self):
        return self.pii_uuid

    def set_lastname(self, lastname):
        self.lastname = lastname

    def get_lastname(self):
        return self.lastname

    def set_firstname(self, firstname):
        self.firstname = firstname

    def get_firstname(self):
        return self.firstname

    def set_phone(self, phone):
        self.phone = phone

    def get_phone(self):
        return self.phone

    def set_email(self, email):
        self.email = email

    def get_email(self):
        return self.email

    def set_username(self, username):
        self.username = username

    def get_username(self):
        return self.username

    def set_uin(self, uin):
        self.uin = uin

    def get_uin(self):
        return self.uin

    def add_uuid(self, uuid):
        if (uuid != None):
            self.get_uuid().append(uuid)

    def set_uuid(self, uuid):
        self.uuid = uuid

    def get_uuid(self):
        return self.uuid

    def set_first_modified_date(self, first_modified_date):
        self.first_modified_date = first_modified_date

    def get_first_modified_date(self):
        return self.first_modified_date

    def set_last_modified_date(self, last_modified_date):
        self.last_modified_date = last_modified_date

    def get_last_modified_date(self):
        return self.last_modified_date