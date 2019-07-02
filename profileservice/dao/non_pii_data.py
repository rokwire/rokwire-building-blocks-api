import profileservice.restservice.utils.datasetutils as datasetutils

class NonPiiData():
    def __init__(self, injson):
        self.uuid = None
        self.interests = None
        self.favorites = None
        self.over13 = None
        self.interestTags = None
        self.creationDate = None
        self.lastModifiedDate = None

        self = datasetutils.update_non_pii_dataset_from_json(self, injson)

    def set_uuid(self, uuid):
        self.uuid = uuid

    def get_uuid(self):
        return self.uuid

    def set_over13(self, over13):
        self.over13 = over13

    def get_over13(self):
        return self.over13

    def add_interests(self, interest):
        if (interest is not None):
            self.get_interests().append(interest)

    def set_interests(self, interests):
        self.interests = interests

    def get_interests(self):
        return self.interests

    def set_favorites(self, favorites):
        self.favorites = favorites

    def get_favorites(self):
        return self.favorites

    def add_interestTags(self, interestTags):
        if (interestTags is not None):
            self.get_interestTags().append(interestTags)

    def set_interestTags(self, interestTags):
        self.interestTags = interestTags

    def get_interestTags(self):
        return self.interestTags

    def set_creation_date(self, creationDate):
        self.creationDate = creationDate

    def get_creation_date(self):
        return self.creationDate

    def set_last_modified_date(self, lastModifiedDate):
        self.lastModifiedDate = lastModifiedDate

    def get_last_modified_date(self):
        return self.lastModifiedDate