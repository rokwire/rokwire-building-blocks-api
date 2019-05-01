import uuid

class non_pii_data:
    def __init__(self, injson):
        self.uuid = None
        self.general_interests = None
        self.athletics_interests = None
        self.file_descriptors = None
        self.image_uri = None

        try:
            self.set_uuid(injson["uuid"])
        except:
            self.set_uuid(str(uuid.uuid4()))
        try:
            self.set_file_descriptors(injson['file_descriptors'])
        except:
            pass
        try:
            self.set_image_uri(injson['image_uri'])
        except:
            pass
        try:
            self.set_general_interests(injson["general_interests"])
        except Exception as e:
            pass
        try:
            self.set_athletics_interests(injson["athletics_interests"])
        except Exception as e:
            pass

    def get_uuid(self):
        return self.uuid

    def set_uuid(self, uuid):
        self.uuid = uuid

    def set_general_interests(self, general_interests):
        self.general_interests = general_interests

    def get_general_interests(self):
        return self.general_interests

    def add_general_interests(self, general_interests):
        if (general_interests is not None):
            self.get_general_interests().append(general_interests)
    def set_athletics_interests(self, athletics_interests):
        self.athletics_interests = athletics_interests

    def get_athletics_interests(self):
        return self.athletics_interests

    def add_athletics_interests(self, athletics_interests):
        if (athletics_interests is not None):
            self.get_athletics_interests().append(athletics_interests)

    def add_file_descriptor(self, file_descriptor):
        if (file_descriptor is not None):
            self.get_file_descriptors().append(file_descriptor)

    def set_file_descriptors(self, file_descriptors):
        self.file_descriptors = file_descriptors

    def get_file_descriptors(self):
        return self.file_descriptors

    def set_image_uri(self, image_uri):
        self.image_uri = image_uri

    def get_image_uri(self):
        return self.image_uri

