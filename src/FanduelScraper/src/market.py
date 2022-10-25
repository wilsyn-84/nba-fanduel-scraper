from src.event import Event
from src.runner import Runner
import pandas as pd
import datetime

class Market:
    def __init__(self, market_details, event_details):
        self.event_type_id = market_details.get('eventTypeId')
        self.competition_id = market_details.get('competitionId')
        self.event_id = market_details.get('eventId')
        self.events = {eid:Event(event_details[eid]) for eid in event_details}
        self.market_id = market_details.get('marketId')
        self.market_name = market_details.get('marketName')
        self.market_time = market_details.get('marketTime')
        self.market_type = market_details.get('marketType')
        self.number_of_runners = market_details.get('numberOfRunners')
        self.number_of_active_runners = market_details.get('numberOfActiveRunners')
        self.number_of_winners = market_details.get('numberOfWinners')
        self.bsp_market = market_details.get('bspMarket')
        self.sgm_market = market_details.get('sgmMarket')
        self.betting_type = market_details.get('bettingType')
        self.market_status = market_details.get('marketStatus')
        self.in_play = market_details.get('inPlay')
        self.sort_priority = market_details.get('sortPriority')
        self.runners = [Runner(r) for r in market_details.get('runners')]
        self.can_turn_in_play = market_details.get('canTurnInPlay')
        self.associated_markets = market_details.get('associatedMarkets') ## we can create events form these I think
        self.has_cashout = market_details.get('hasCashout')
        self.eachway_available = market_details.get('eachwayAvailable')
        self.leg_types = market_details.get('legTypes')
        #print(self.events)

    def to_df(self):
        '''
        :return: Pandas DataFrame
        This function will create one row per RUNNER (not market)
        '''
        return pd.DataFrame([dict(self.to_dict(), **runner.to_dict()) for runner in self.runners])

    def to_dict(self):
        '''
        :return: converts obj to a dictionary - refined for `to_df()` func
        '''
        print(self.events[str(self.event_id)].event_name)
        return {
            "event_id": self.event_id,
            "event_name": self.events[str(self.event_id)].event_name,
            "market_id": self.market_id,
            "market_name": self.market_name,
            "market_time": self.market_time,
            "market_type": self.market_type,
            "sgm_market": self.sgm_market,
            "betting_type": self.betting_type,
            "market_start_date": datetime.datetime
                .strptime(self.market_time, '%Y-%m-%dT%H:%M:%S.%fZ')
                .strftime('%Y-%m-%d'),
        }

    def __str__(self):
        return "{self.market_id} - {self.market_name}".format(self=self)

