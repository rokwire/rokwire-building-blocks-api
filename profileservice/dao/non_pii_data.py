"""
author: Yong Wook Kim
created 2019 Apr 4
"""
import uuid

class non_pii_data:
    def __init__(self):
        self.objectid = None
        self.genetral_interests = None
        self.athletics_interests = None

    def set_objectid(self, objectid):
        self.objectid = objectid

    def get_objectid(self):
        return self.objectid

    def set_genetral_interests(self, genetral_interests):
        self.genetral_interests = genetral_interests

    def get_genetral_interests(self):
        return self.genetral_interests

    def add_genetral_interests(self, genetral_interests):
        if (genetral_interests != None):
            self.get_genetral_interests().append(genetral_interests)
    def set_athletics_interests(self, athletics_interests):
        self.athletics_interests = athletics_interests

    def get_athletics_interests(self):
        return self.athletics_interests

    def add_athletics_interests(self, athletics_interests):
        if (athletics_interests != None):
            self.get_athletics_interests().append(athletics_interests)