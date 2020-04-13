class DataDeletionApiEndpoint:
    def __init__(self, injson):
        self.uuid = None
        self.check = None

    def set_uuid(self, uuid):
        self.uuid = uuid

    def get_uuid(self):
        return self.uuid

    def set_check(self, check):
        self.check = check

    def get_check(self):
        return self.check
