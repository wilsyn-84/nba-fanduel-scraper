import requests
import datetime
from src.Event import Event

class Scaper:
    def __init__(self, sport, sport_configs):
        self.sport = sport
        self.sport_configs = sport_configs
        self.api_urls = {
            "wager_event": 'https://tn.sportsbook.fanduel.com/cache/psmg/UK/{}.json',
            "wager_event_details": 'https://tn.sportsbook.fanduel.com/cache/psevent/UK/1/false/{}.json'
        }
        self.date = datetime.date.today().strftime("%Y-%m-%d")

    def download_data(self):
        events = self.get_todays_events()
        event_details = []
        for eventType in events['events']:
            for e in events['events'][eventType]:
                event = Event(e)
                event_details.append(self.get_event_details(event, self.sport_configs[eventType]['details']))

        selections_list = [selection for event in event_details for selection in event['selections']]
        event_details_response_list = [resp for event in event_details for resp in event['response']]

        return {
            "selections": selections_list,
            "events_response": events['events'],
            "event_details_response": event_details_response_list
        }

    def get_todays_events(self):
        wagerEvents = {}
        events = {}
        for event in self.sport_configs:
            print(event)
            code = self.sport_configs[event]['code']
            resp = requests.get(self.api_urls['wager_event'].format(code))
            wagerEvent_resp = resp.json()

            events[event] = wagerEvent_resp.get('events')
            wagerEvents[event] = wagerEvent_resp

        return {
            "wagerEvents": wagerEvents,
            "events": events
        }

    def get_event_details(self, event: Event, fetchDetails: bool):
        print("Getting Details for ", event.desc)
        if fetchDetails:
            print('Fetching Details')
            resp = requests.get(self.api_urls['wager_event_details'].format(event.eventId))
            try:
                eventmarketgroups = resp.json()['eventmarketgroups']
            except:
                print('probably in progress - no eventmarketgroup data')
                return {"response": [], "selections": []}
        else:
            eventmarketgroups = event.eventMarketGroups

        selections = []
        for event_category in eventmarketgroups:
            # Skip individual groups and grab everything in the 'All' category
            if event_category['name'] != 'All':
                continue
            for market in event_category['markets']:
                for selection in market['selections']:
                    selections.append({
                        "gameStartDate": datetime.datetime
                            .strptime(market['tsstart'], '%Y-%m-%dT%H:%M:%S')
                            .strftime('%Y-%m-%d'),
                        "gameDesc": event.desc,
                        "gameId": event.eventId,
                        "gameStartTs": market['tsstart'],
                        "marketName": market['name'],
                        "marketId": market['idfomarket'],
                        "marketType": market.get('markettypename') or market.get('name'),  ## null or??
                        "marketTypeId": market['idfomarkettype'],
                        "marketTypeCode": market.get('idfohadtype'),
                        "selectionName": selection['name'],
                        "selectionId": selection['idfoselection'],
                        "currentHandicap": self.calculate_handicap(selection),
                        "value": self.calculate_wager_odds(selection['currentpriceup'], selection['currentpricedown']),
                        "hadvalue": selection.get('hadvalue'),
                        "scrape_ts": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
        print('Done')
        return {"response": eventmarketgroups, "selections": selections}

    def calculate_wager_odds(self, up, down):
        if up > down:
            return (up / down) * 100
        else:
            return -100 / (up / down)

    def calculate_handicap(self, selection):
        if selection.get('currenthandicap'):
            if selection['hadvalue'] == 'A':
                return selection['currenthandicap']*-1
            else:
                return selection['currenthandicap']
        else:
            return None
