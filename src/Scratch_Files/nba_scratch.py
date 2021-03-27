from nba_api.TeamBoxScores import TeamBoxScores
tbs = TeamBoxScores()

#df = tbs.get_boxscores(types=['base'], seasons = ['2019-20','2020-21'])

df = tbs.get_boxscores(types=['base','advanced','four factors','misc', 'scoring'],
                       seasons = ['2012-13','2013-14','2014-15','2015-16','2016-17','2017-18','2018-19','2019-20','2020-21'])

df.to_csv("data.csv")


'''
import requests
import pandas as pd

url = "https://stats.nba.com/stats/teamgamelogs?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlusMinus=N&Rank=N&Season=2020-21&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&VsConference=&VsDivision="
url = "https://stats.nba.com/stats/teamgamelogs?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlusMinus=N&Rank=N&Season=2020-21&SeasonSegment=&SeasonType=Regular Season&ShotClockRange=&VsConference=&VsDivision="


url = "https://stats.nba.com/stats/teamgamelogs"

params = {
    "DateFrom":"",
    "DateTo":"",
    "GameSegment":"",
    "LastNGames":"0",
    "LeagueID":"00",
    "Location":"",
    "MeasureType":"Advanced",
    "Month":"0",
    "OpponentTeamID":"0",
    "Outcome":"",
    "PORound":"0",
    "PaceAdjust":"N",
    "PerMode":"Totals",
    "Period":"0",
    "PlusMinus":"N",
    "Rank":"N",
    "Season":"2020-21",
    "SeasonSegment":"",
    "SeasonType":"Regular Season",
    "ShotClockRange":"",
    "VsConference":"",
    "VsDivision":""
}

headers = {
  'Accept': 'application/json, text/plain, */*',
  'Accept-Encoding': 'gzip, deflate, br',
  'Accept-Language': 'en-US,en;q=0.9',
  'Cache-Control': 'no-cache',
  'Connection': 'keep-alive',
  'Host': 'stats.nba.com',
  'Origin': 'https://www.nba.com',
  'Pragma': 'no-cache',
  'Referer': 'https://www.nba.com/',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-site',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
  'x-nba-stats-origin': 'stats',
  'x-nba-stats-token': 'true',
  'Cookie': 'ak_bmsc=297000FE356F6E9CA699E8005D52FE6D172CAA21161900003FC3F35FCD4B3D52~pleA00MDVnoJXNASAhurKHtPSG3wg08bkMxAmiiJiAp1hI+1DjYrj8+YR70GhH9gxQRKOSLpSNQkv9LFhqe71KS9MatD3+9bCx5QI9kNG1IcsuCS7dCMkEgPwbAT1+lPPVCCDq+AsB78skuQu1qujIzpAbJfvMVZPwxdZJJhfuW6o9rP0SHoPzARqnKolgxH//6uovhXw24DHk0uT3hz0WMio8XaaAyEhoSqKf8gVuWbk='
}

response = requests.request("GET", url, headers=headers, params = params)

data = response.json()

df = pd.DataFrame(data=data['resultSets'][0]['rowSet'], columns=data['resultSets'][0]['headers'])
'''

'''
import requests
from NBA.Game import Game
print("Getting Todays Games")
print('NBA')
response = requests.get('https://tn.sportsbook.fanduel.com/cache/psmg/UK/63747.3.json')

todays_games = []
for event in response.json()['events']:
    game = Game(event)
    print(game)
    todays_games.append(game)

games_dict = {}
for game in todays_games:
    print(game)
    response = requests.get('https://tn.sportsbook.fanduel.com/cache/psevent/UK/1/false/{}.json'.format(game.eventId))
    response_data = response.json()
    games_dict[game.eventId] = response_data

    selection_dict = {}
    types = set()
    for event_market in response_data['eventmarketgroups']:
        #print("Market Category:", event_market['name'])
        if event_market['name'] != 'All':
            continue
        #print("Market Category:", event_market['name'])
        for market in event_market['markets']:
            #print(market.get('idfohadtype'))
            #types.add(market.get('idfohadtype'))
            types.add(market.get('markettypename'))
            print("Market Type:", market['name'])
            for selection in market['selections']:
                #print(str(selection['idfoselection']) + ' - ' + selection['name'])
                if selection['currentpriceup'] > selection['currentpricedown']:
                    odds = (selection['currentpriceup'] / selection['currentpricedown'])*100
                else:
                    odds = -100 / (selection['currentpriceup'] / selection['currentpricedown'])
                selection_dict[selection['idfoselection']] = {
                    "Game": game.desc,
                    "selectionName": selection['name'],
                    "currentHandicap": selection.get('currenthandicap'),
                    "currentpriceup": selection['currentpriceup'],
                    "currentpricedown": selection['currentpricedown'],
                    "value": odds,
                    "hadvalue": selection.get('hadvalue'),
                    "selectionhashcode": selection['selectionhashcode'],
                    "marketType": market['name'],
                    "marketCategory": event_market['name']
                }

        if selection.get('currenthandicap'):
            if selection['hadvalue'] == 'A':
                return selection['currenthandicap']*-1
            else:
                return selection['currenthandicap']
        else:
            return None

    'https://tn.sportsbook.fanduel.com/sports/event/947169.3'

# game
# market type
# selections
'''