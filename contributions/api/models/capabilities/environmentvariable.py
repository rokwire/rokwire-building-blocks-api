class EnvironmentVariable:
    def __init__(self):
        self.key = None
        self.value = None

    def set_key(self, key):
        self.key = key

    def get_key(self):
        return self.key

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value
