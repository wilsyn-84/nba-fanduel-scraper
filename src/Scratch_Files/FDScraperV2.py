import requests
import json
import pandas as pd
from datetime import datetime
import pytz

url = "https://sbapi.tn.sportsbook.fanduel.com/api/content-managed-page?betexRegion=GBR&capiJurisdiction=intl&currencyCode=USD&exchangeLocale=en_US&includePrices=true&includeRaceCards=false&includeSeo=true&language=en&regionCode=NAMERICA&timezone=America%2FChicago&includeMarketBlurbs=true&_ak=FhMFpcPWXMeyZxOx&page=CUSTOM&customPageId=nfl"

payload={}
headers = {
  'Cookie': 'X-Sportsbook-Region=tn'
}

response = requests.request("GET", url, headers=headers, data=payload)
resp = response.json()

markets = resp['attachments']['markets']
eventTypes = resp['attachments']['eventTypes']
competitions = resp['attachments']['competitions']
events = resp['attachments']['events']

team_map = {
'Arizona Cardinals': 'ARI Cardinals',
'Atlanta Falcons': 'ATL Falcons',
'Baltimore Ravens': 'BAL Ravens',
'Buffalo Bills': 'BUF Bills',
'Carolina Panthers': 'CAR Panthers',
'Chicago Bears': 'CHI Bears',
'Cincinnati Bengals': 'CIN Bengals',
'Cleveland Browns': 'CLE Browns',
'Dallas Cowboys': 'DAL Cowboys',
'Denver Broncos': 'DEN Broncos',
'Detroit Lions': 'DET Lions',
'Green Bay Packers': 'GB Packers',
'Houston Texans': 'HOU Texans',
'Indianapolis Colts': 'IND Colts',
'Jacksonville Jaguars': 'JAX Jaguars',
'Kansas City Chiefs': 'KC Chiefs',
'Las Vegas Raiders': 'LV Raiders',
'Los Angeles Chargers': 'LAC Chargers',
'Los Angeles Rams': 'LA Rams',
'Miami Dolphins': 'MIA Dolphins',
'Minnesota Vikings': 'MIN VIkings',
'New England Patriots': 'NE Patriots',
'New Orleans Saints': 'NO Saints',
'New York Giants': 'NY Giants',
'New York Jets': 'NYJ Jets',
'Philadelphia Eagles': 'PHI Eagles',
'Pittsburgh Steelers': 'PIT Steelers',
'San Francisco 49ers': 'SF 49ers',
'Seattle Seahawks': 'SEA Seahawks',
'Tampa Bay Buccaneers': 'TB Buccaneers',
'Tennessee Titans': 'TEN Titans',
'Washington Football Team': 'WAS Football Team',
}

data = []
for market in markets:
    for runner in markets[market]['runners']:
        if markets[market]['marketName'] in ['Moneyline','Spread','Total Match Points']:
            print("{} - {} - {} - {} - {}".format(
                eventTypes[str(markets[market]['eventTypeId'])]['name'],
                competitions[str(markets[market]['competitionId'])]['name'],
                events[str(markets[market]['eventId'])]['name'],
                markets[market]['marketName'],
                runner['runnerName']))


            if runner['runnerName'] == 'Over':
                team = events[str(markets[market]['eventId'])]['name'].split(" @ ")[0]
                loc = 'away'
            elif runner['runnerName'] == 'Under':
                team = events[str(markets[market]['eventId'])]['name'].split(" @ ")[1]
                loc = 'home'
            else:
                team = runner['runnerName']

            if markets[market]['marketName'] == 'Moneyline':
                value = str(runner['winRunnerOdds']['americanDisplayOdds']['americanOdds'])
            elif markets[market]['marketName'] == 'Total Match Points':
                if runner['runnerName'] == 'Over':
                    value = str(runner['handicap']) + " O"
                else:
                    value = str(runner['handicap']) + " U"
            else:
                value = runner['handicap']

            data.append({
                "eventType": eventTypes[str(markets[market]['eventTypeId'])]['name'],
                "competition": competitions[str(markets[market]['competitionId'])]['name'],
                "event": events[str(markets[market]['eventId'])]['name'],
                "marketName": markets[market]['marketName'],
                "marketTime": pd.to_datetime(markets[market]['marketTime']).tz_convert(pytz.timezone('US/Central')).strftime("%D"),
                "selectionId": runner['selectionId'],
                "selectionName": runner['runnerName'],
                "handicap": runner['handicap'],
                "selectionOdds": runner['winRunnerOdds']['americanDisplayOdds']['americanOdds'],
                "team": team_map[team],
                "value": value,
            })

df = pd.DataFrame(data)

pivot = df.pivot_table(index=['marketTime', 'event', 'team'],
                       columns='marketName',
                       values='value',
                       aggfunc='first'
                       ).reset_index()
pivot['W'] = 0
pivot.columns
pivot = pivot.sort_values(by = ['marketTime', 'event','Total Match Points']).reset_index()
pivot = pivot[['marketTime','event','team','W','Spread','Moneyline',"Total Match Points"]]
pivot.to_csv('wk4.csv')

with open('wk4_response_dump.json', 'w') as outfile:
    json.dump(resp, outfile)
##########################################################################

with open('wk4_response_dump.json', 'r') as outfile:
    data = json.load(outfile)

markets = data['attachments']['markets']
eventTypes = data['attachments']['eventTypes']
competitions = data['attachments']['competitions']
events = data['attachments']['events']


event_ids = []
for market in markets:
    for runner in markets[market]['runners']:
        if competitions[str(markets[market]['competitionId'])]['name'] == 'NFL' and 'Matches' not in events[str(markets[market]['eventId'])]['name']:
            print("{} - {} - {} - {} - {} - {}".format(
                events[str(markets[market]['eventId'])]['eventId'],
                eventTypes[str(markets[market]['eventTypeId'])]['name'],
                competitions[str(markets[market]['competitionId'])]['name'],
                events[str(markets[market]['eventId'])]['name'],
                markets[market]['marketName'],
                runner['runnerName']))
            event_ids.append(events[str(markets[market]['eventId'])]['eventId'])

event_id = events[str(markets[market]['eventId'])]['eventId']
# Event ID Search
event_url = 'https://sbapi.tn.sportsbook.fanduel.com/api/event-page?betexRegion=GBR&capiJurisdiction=intl&currencyCode=USD&exchangeLocale=en_US&includePrices=true&language=en&priceHistory=1&regionCode=NAMERICA&usePlayerPropsVirtualMarket=true&_ak=FhMFpcPWXMeyZxOx&eventId={}'.format(30929773)
payload={}
headers = {
  'Cookie': 'X-Sportsbook-Region=tn'
}

response = requests.request("GET", event_url, headers=headers, data=payload)
resp = response.json()

markets = resp['attachments']['markets']
eventTypes = resp['attachments']['eventTypes']
competitions = resp['attachments']['competitions']
events = resp['attachments']['events']

for market in markets:
    for runner in markets[market]['runners']:
        if competitions[str(markets[market]['competitionId'])]['name'] == 'NFL' and 'Matches' not in events[str(markets[market]['eventId'])]['name']:
            print("{} - {} - {} - {} - {} - {}".format(
                events[str(markets[market]['eventId'])]['eventId'],
                eventTypes[str(markets[market]['eventTypeId'])]['name'],
                competitions[str(markets[market]['competitionId'])]['name'],
                events[str(markets[market]['eventId'])]['name'],
                markets[market]['marketName'],
                runner['runnerName']))
