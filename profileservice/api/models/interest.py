class Interest():
    def __init__(self):
        self.category = None
        self.subcategories = None

    def set_category(self, category):
        self.category = category

    def get_category(self):
        return self.category

    def add_subcategories(self, subcategory):
        if (subcategory is not None):
            self.get_subcategories().append(subcategory)

    def set_subcategories(self, subcategories):
        self.subcategories = subcategories

    def get_subcategories(self):
        return self.subcategories