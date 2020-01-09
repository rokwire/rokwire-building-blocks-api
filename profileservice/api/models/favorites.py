class Favorites():
    def __init__(self):
        self.eventIds = None
        self.placeIds = None
        self.diningPlaceIds = None
        self.laundryPlaceIds = None
        self.athleticEventIds = None

    def set_eventIds(self, eventIds):
        self.eventIds = eventIds

    def get_eventIds(self):
        return self.eventIds

    def add_eventId(self, eventId):
        if (eventId is not None):
            self.get_eventIds().append(eventId)

    def set_placeIds(self, placeIds):
        self.placeIds = placeIds

    def get_placeIds(self):
        return self.placeIds

    def add_placeId(self, placeId):
        if (placeId is not None):
            self.get_placeIds().append(placeId)

    def set_diningPlaceIds(self, diningPlaceIds):
        self.diningPlaceIds = diningPlaceIds

    def get_diningPlaceIds(self):
        return self.diningPlaceIds

    def add_diningPlaceId(self, diningPlaceId):
        if (diningPlaceId is not None):
            self.get_diningPlaceIds().append(diningPlaceId)

    def set_laundryPlaceIds(self, laundryPlaceIds):
        self.laundryPlaceIds = laundryPlaceIds

    def get_laundryPlaceIds(self):
        return self.laundryPlaceIds

    def add_laundryPlaceId(self, laundryPlaceId):
        if (laundryPlaceId is not None):
            self.get_laundryPlaceIds().append(laundryPlaceId)

    def set_athleticEventIds(self, athleticEventIds):
        self.athleticEventIds = athleticEventIds

    def get_athleticEventIds(self):
        return self.athleticEventIds

    def add_athleticEventId(self, athleticEventId):
        if (athleticEventId is not None):
            self.get_athleticEventIds().append(athleticEventId)