class DataDeletionEndpointDetails:
    def __init__(self):
        self.deletionEndpoint = None
        self.apiKey = None

    def set_deletion_endpoint(self, deletionEndpoint):
        self.deletionEndpoint = deletionEndpoint

    def get_deletion_endpoint(self):
        return self.deletionEndpoint

    def set_api_key(self, apiKey):
        self.apiKey = apiKey

    def get_api_key(self):
        return self.apiKey
