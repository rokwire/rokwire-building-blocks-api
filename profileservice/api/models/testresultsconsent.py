class TestResultsConsent():
    def __init__(self):
        self.consentProvided  = None
        self.dateModified   = None

    def set_consent_provided(self, consentProvided ):
        self.consentProvided  = consentProvided

    def get_consent_provided(self):
        return self.consentProvided

    def set_date_modified(self, dateModified ):
        self.dateModified  = dateModified

    def get_date_modified(self):
        return self.dateModified