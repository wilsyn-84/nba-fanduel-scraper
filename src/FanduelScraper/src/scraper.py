import datetime
import pandas as pd
from src.event import Event
from src.market import Market
import src.helpers as helpers

class Scaper:
    def __init__(self, sport):
        self.sport = sport
        self.api_url = "https://sbapi.tn.sportsbook.fanduel.com/api/{}"
        self.api_query_params = [
            ("betexRegion", "GBR"),
            ("capiJurisdiction", "intl"),
            ("currencyCode", "USD"),
            ("exchangeLocale", "en_US"),
            ("includePrices", "true"),
            ("language", "en"),
            ("regionCode", "NAMERICA"),
            ("timezone", "America%2FChicago"),
            ("_ak", "FhMFpcPWXMeyZxOx")
        ]
        self.date = datetime.date.today().strftime("%Y-%m-%d")
        self.request_responses = {
            "event": [],
            "event_details": {}
        }

    def get_available_events(self):
        print('Getting Available Events')
        url = self.api_url.format("content-managed-page")
        params = self.api_query_params + [
            ("page", "CUSTOM"),
            ("customPageId", self.sport)
        ]
        response = helpers.make_request(url, params)
        if response.status_code == 200:
            event_ids = self._parse_event_ids(response.json())
            self.request_responses['event'].append(response.json())
        else:
            event_ids = []
            print('Response Code: {}'.format(response.status_code))
        return event_ids

    def _parse_event_ids(self, response):
        '''
        :param response: request response.json()
        :return: list of event_ids (str).
        '''
        attachments = response.get('attachments')
        competitions = attachments['competitions']
        events = attachments['events']

        # For some reason, a generic event_id for a specific competition (i.e. NBA / Basketball) is returned
        # and we want to exclude that from the returned list
        competition_event_ids = [str(c['eventId']) for c in competitions.values()]
        event_ids = [event for event in events if event not in competition_event_ids]
        return event_ids

    def get_event_details(self, event_id):
        '''
        :param event_id: str
        :return: Pandas DataFrame for specific event
        '''
        print('Getting Event Details - {}'.format(event_id))
        url = self.api_url.format("event-page")
        params = self.api_query_params + [
            ("usePlayerPropsVirtualMarket", "true"),
            ("eventId", event_id)
        ]
        response = helpers.make_request(url, params)
        self.request_responses['event_details'][event_id] = response.json()
        markets = self._parse_event_details(response.json())
        df = self._markets_to_df(markets)
        return df

    def _parse_event_details(self, response):
        '''
        :param response: request response.json()
        :return: list of Market objs
        '''
        attachments = response.get('attachments')
        events = attachments['events']
        markets = attachments['markets']

        ## I want to pass the event info into the market so I can build a more robust df
        return [Market(market, events) for market in markets.values()]

    def _markets_to_df(self, markets):
        '''
        :param markets: list of Market objs
        :return: a single df with all available markets for an event
        '''
        df_list = [market.to_df() for market in markets]
        return pd.concat(df_list, ignore_index=True) if len(df_list) > 0 else pd.DataFrame()

    def download_data(self):
        '''
        This is the 'main' function for this class.  It will call the Fanduel API to get the available events
        for the given object's sport.  Then for each event, it will get all available markets for that event.
        The resulting obj will be a dataframe with all markets for all available events
        :return: Pandas DataFrame
        '''
        event_ids = self.get_available_events()
        event_details_dfs = [self.get_event_details(id) for id in event_ids]
        df = pd.concat(event_details_dfs)
        return {
            "selections": df,
            "responses": self.request_responses
        }
