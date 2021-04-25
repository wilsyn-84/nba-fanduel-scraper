
class Event:
    def __init__(self, details):
        self.details = details
        self.desc = details.get('externaldescription')
        self.eventId = str(details.get('idfoevent'))
        self.sportLeague = details.get('sportname')
        self.sportType = details.get('idfosporttype')
        self.startTime = details.get('tsstart')
        self.eventMarketGroups = [{"name": "All", "markets": details.get('markets')}]
        self.eventMarkets = details.get('markets')
        #self.eventMarkets = []

    def extract_markets(self):
        return ''

    def add_wager(self):
        return ''
    def add_market(self, market):
        self.eventMarkets.append(market)

    def __str__(self):
        return self.eventId + " - " + self.desc