class PrivacySettings():
    def __init__(self):
        self.level = None
        self.dateModified = None

    def set_level(self, level):
        self.level = level

    def get_level(self):
        return self.level

    def set_date_modified(self, dateModified):
        self.dateModified = dateModified

    def get_date_modified(self):
        return self.dateModified