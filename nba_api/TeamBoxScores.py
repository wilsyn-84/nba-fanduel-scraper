import requests
import pandas as pd
import functools

class TeamBoxScores:
    def __init__(self):
        self.url = "https://stats.nba.com/stats/teamgamelogs"
        self.params = {
            "DateFrom":"",
            "DateTo":"",
            "GameSegment":"",
            "LastNGames":"0",
            "LeagueID":"00",
            "Location":"",
            "MeasureType":"",
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
        self.headers = {
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
 #           'Cookie': 'ak_bmsc=297000FE356F6E9CA699E8005D52FE6D172CAA21161900003FC3F35FCD4B3D52~pleA00MDVnoJXNASAhurKHtPSG3wg08bkMxAmiiJiAp1hI+1DjYrj8+YR70GhH9gxQRKOSLpSNQkv9LFhqe71KS9MatD3+9bCx5QI9kNG1IcsuCS7dCMkEgPwbAT1+lPPVCCDq+AsB78skuQu1qujIzpAbJfvMVZPwxdZJJhfuW6o9rP0SHoPzARqnKolgxH//6uovhXw24DHk0uT3hz0WMio8XaaAyEhoSqKf8gVuWbk='
        }

    def get_boxscores(self, types=['base'], seasons=['2020-21']):
        boxscores = {}
        for season in seasons:
            print('Season: {}'.format(season))
            for type in types:
                print("Getting {} Boxscore".format(type))
                data = self.call_api(params=self.set_params(type, season))
                boxscores.setdefault(type, []).append(self.clean_df_columns(data))
                #boxscores[type].append(self.clean_df_columns(data))
        return self.merge_boxscores(boxscores)

    def call_api(self, params):
        response = requests.request("GET", self.url, headers=self.headers, params=params)
        data = response.json()
        df = pd.DataFrame(data=data['resultSets'][0]['rowSet'], columns=data['resultSets'][0]['headers'])
        return df

    def set_params(self, measureType, season):
        p = self.params
        type = self.find_measureType(measureType)
        p['MeasureType'] = type
        p['Season'] = season
        return p

    def find_measureType(self, type):
        if type.lower() == 'base':
            return 'Base'
        if type.lower() == 'advanced':
            return 'Advanced'
        if type.lower() == 'four factors':
            return 'Four Factors'
        if type.lower() == 'misc':
            return 'Misc'
        if type.lower() == 'scoring':
            return 'Scoring'
        else:
            raise ValueError("Valid types are: ['Base','Advanced','Four Factors','Misc','Scoring'] ")

    def clean_df_columns(self, df):
        cols = [c for c in df.columns if 'rank' not in c.lower()]
        return df[cols]

    def merge_boxscores(self, df_dict):
        print('Merging DFs')
        df_list = []
        for key, dfs in df_dict.items():
            df_list.append(pd.concat(dfs))
        return functools.reduce(
            lambda left, right:
            pd.merge(left, right, on=list(set(left.columns).intersection(set(right.columns))))
            , df_list)
