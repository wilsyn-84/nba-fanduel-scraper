import requests
from NBA.Game import Game
#import pandas as pd
import datetime

class NBAScapper:
    def __init__(self):
        self.api_urls = {
            "games": 'https://tn.sportsbook.fanduel.com/cache/psmg/UK/63747.3.json',
            "game_details": 'https://tn.sportsbook.fanduel.com/cache/psevent/UK/1/false/{}.json'
        }
        self.date = datetime.date.today().strftime("%Y-%m-%d")

    def download_today_games(self):
        games = self.get_todays_games()
        game_details = []
        for game in games:
            game_details.append(self.get_game_details(game))

        print("Flattening List")
        flat_list = [selection for game in game_details for selection in game]
        print('Creating DF')
        return flat_list
        #df = pd.DataFrame(flat_list)
        #self.save_games(df)

    def save_games(self,df, filename):
        print("Saving")
        #df.to_csv(self.filename, index=False)

    def get_todays_games(self):
        print("Getting Todays Games")
        resp = requests.get(self.api_urls['games'])
        games = []
        for event in resp.json()['events']:
            game = Game(event)
            print(game)
            games.append(game)
        return games

    def get_game_details(self, game):
        resp = requests.get(self.api_urls['game_details'].format(game.eventId))
        selections = []
        print("Getting Details for ", game.desc) 
        try:
            #eventmarketgroups
            #print(resp.json())
            eventmarketgroups = resp.json()['eventmarketgroups']
        except:
            print('probably in progress - no eventmarketgroup data')
            return selections
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
                        "gameDesc": game.desc,
                        "gameId": game.eventId,
                        "gameStartTs": market['tsstart'],
                        "marketName": market['name'],
                        "marketId": market['idfomarket'],
                        "marketType": market['markettypename'],
                        "marketTypeId": market['idfomarkettype'],
                        "marketTypeCode": market.get('idfohadtype'),
                        "selectionName": selection['name'],
                        "selectionId": selection['idfoselection'],
                        #"currentHandicap": selection.get('currenthandicap'),
                        "currentHandicap": self.calculate_handicap(selection),
                        "value": self.calculate_wager_odds(selection['currentpriceup'], selection['currentpricedown']),
                        "hadvalue": selection.get('hadvalue'),
                        "scrape_ts": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
        print('Done')
        return selections

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