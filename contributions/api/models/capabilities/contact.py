class Contact:
    def __init__(self):
        self.name = None
        self.email = None
        self.phone = None
        self.organization = None
        self.officialAddress = None

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_email(self, email):
        self.email = email

    def get_email(self):
        return self.email

    def set_phone(self, phone):
        self.phone = phone

    def get_phone(self):
        return self.phone

    def set_organization(self, organization):
        self.organization = organization

    def get_organization(self):
        return self.organization

    def set_officialAddress(self, officialAddress):
        self.officialAddress = officialAddress

    def get_officialAddress(self):
        return self.officialAddress