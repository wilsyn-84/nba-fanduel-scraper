class Event:
    def __init__(self, details):
        self.competition_id = details.get("competitionId")
        self.event_id = details.get('eventId')
        self.event_name = details.get('name')
        self.event_type_id = details.get('eventTypeId')
        self.country_code = details.get('countryCode')
        self.timezone = details.get('timezone')
        self.open_date = details.get('openDate')
        self.in_play = details.get('inPlay')
        self.key = details.get('key')
        self.video_available = details.get('videoAvailable')
        self.primary_market = details.get('primaryMarketId')

    def __str__(self):
        return "{self.event_id} - {self.event_name}".format(self=self)

'''
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
'''