import pandas as pd
import requests
api_urls = {
            "wager_event": 'https://tn.sportsbook.fanduel.com/cache/psmg/UK/{}.json',
            "wager_event_details": 'https://tn.sportsbook.fanduel.com/cache/psevent/UK/1/false/{}.json'
        }
url = "https://sbapi.tn.sportsbook.fanduel.com/api/content-managed-page?betexRegion=GBR&capiJurisdiction=intl&currencyCode=USD&exchangeLocale=en_US&includePrices=true&includeRaceCards=false&includeSeo=true&language=en&regionCode=NAMERICA&timezone=America%2FChicago&includeMarketBlurbs=true&_ak=FhMFpcPWXMeyZxOx&page=CUSTOM&customPageId=nba"
event_details_url = "https://sbapi.tn.sportsbook.fanduel.com/api/event-page?betexRegion=GBR&capiJurisdiction=intl&currencyCode=USD&exchangeLocale=en_US&includePrices=true&language=en&priceHistory=1&regionCode=NAMERICA&usePlayerPropsVirtualMarket=true&_ak=FhMFpcPWXMeyZxOx&eventId={}"
resp = requests.get(url)
resp = resp.json()

markets = resp['attachments']['markets'] #bettable things
eventTypes = resp['attachments']['eventTypes'] #lookup
competitions = resp['attachments']['competitions'] #lookup
events = resp['attachments']['events'] # includes games + categories

#what events do I want to pull?
eventIds = []
for event in events:
    eventType = eventTypes[str(events[event]['eventTypeId'])]['name']
    competitionType = competitions[str(events[event]['competitionId'])]['name']
    if(competitionType == 'NBA' and eventType == 'Basketball'):
        eventIds.append(events[event]['eventId'])
    else:
        print("{} - {}".format(eventType, competitionType))

resp = requests.get(event_details_url.format(eventIds[3]))
resp = resp.json()

#############################################

