class Status():
    def __init__(self):
        self.submitted = None
        self.reviewing = None
        self.approved = None
        self.disapproved = None
        self.pubulished = None

    def set_submitted(self, submitted):
        self.submitted = submitted

    def get_submitted(self):
        return self.submitted

    def set_reviewing(self, reviewing):
        self.reviewing = reviewing

    def get_reviewing(self):
        return self.reviewing

    def set_approved(self, approved):
        self.approved = approved

    def get_approved(self):
        return self.approved

    def set_disapproved(self, disapproved):
        self.disapproved = disapproved

    def get_disapproved(self):
        return self.disapproved

    def set_pubulished(self, pubulished):
        self.pubulished = pubulished

    def get_pubulished(self):
        return self.pubulished