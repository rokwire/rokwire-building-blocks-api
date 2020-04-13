class Status():
    def __init__(self):
        self.submitted = None
        self.inReview = None
        self.approved = None
        self.pubulished = None

    def set_submitted(self, submitted):
        self.submitted = submitted

    def get_submitted(self):
        return self.submitted

    def set_in_review(self, inReview):
        self.inReview = inReview

    def get_in_review(self):
        return self.inReview

    def set_approved(self, approved):
        self.approved = approved

    def get_approved(self):
        return self.approved

    def set_pubulished(self, pubulished):
        self.pubulished = pubulished

    def get_pubulished(self):
        return self.pubulished