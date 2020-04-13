class IfExternallyDeployed():
    def __init__(self):
        self.apiUrl = None

    def set_api_url(self, apiUrl):
        self.apiUrl = apiUrl

    def get_api_url(self):
        return self.apiUrl