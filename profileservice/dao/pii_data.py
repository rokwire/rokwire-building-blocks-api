import uuid

class pii_data:
    def __init__(self, injson):
        self.lastname = None
        self.firstname = None
        self.phone = None
        self.email = None
        self.username = None
        self.uin = None
        self.pii_uuid = None
        self.non_pii_uuid = None
        self.set_pii_uuid(str(uuid.uuid4()))

        try:
            self.set_pii_uuid(injson["pii_uuid"])
        except:
            pass

        try:
            self.set_lastname(injson['lastname'])
        except Exception as e:
            pass
        try:
            self.set_firstname(injson['firstname'])
        except Exception as e:
            pass
        try:
            self.set_phone(injson['phone'])
        except Exception as e:
            pass
        try:
            self.set_email(injson['email'])
        except Exception as e:
            pass
        try:
            self.set_username(injson['username'])
        except Exception as e:
            pass
        try:
            self.set_uin(injson['uin'])
        except Exception as e:
            pass
        try:
            self.set_non_pii_uuid(injson['non_pii_uuid'])
        except Exception as e:
            pass


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

    def add_non_pii_uuid(self, non_pii_uuid):
        if (non_pii_uuid != None):
            self.get_non_pii_uuid().append(non_pii_uuid)

    def set_non_pii_uuid(self, non_pii_uuid):
        self.non_pii_uuid = non_pii_uuid

    def get_non_pii_uuid(self):
        return self.non_pii_uuid