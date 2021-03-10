from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import requests
import base64
import json
import pandas as pd
import pandasql as ps
import datetime

app = Flask(__name__)
CORS(app)

wagers_df = pd.read_csv('Daily_Downloads/wagers.csv')
boxscores_df = pd.read_csv('Boxscores/team_boxscores.csv')
team_lookup_df = pd.read_csv('team_lookup.csv')
today = datetime.date.today().strftime("%Y-%m-%d")

@app.route('/wagers/today', methods = ['GET'])
def get_wagers_today():
    df = wagers_df[
        ( wagers_df['gameStartDate'] == '2021-01-08') &
        ( wagers_df['marketName'].isin(['Moneyline','Spread Betting','Total Points Scored']) )
    ]
    df = df.merge(team_lookup_df, how='left', left_on='selectionName', right_on='fanduel_name')

    dict = {}
    for r in df.iterrows():
        row = r[1]
        gameId = str(row['gameId'])
        dict.setdefault(gameId, {})
        dict[gameId].setdefault('away', {})
        dict[gameId].setdefault('home', {})
        dict[gameId]['gameId'] = gameId
        dict[gameId]['gameStartTs'] = row['gameStartTs']
        dict[gameId]['gameDesc'] = row['gameDesc']
        if row['hadvalue'] in ['A','O']:
            if row['hadvalue'] in ['A']:
                dict[gameId]['away']['team'] = row['selectionName']
                dict[gameId]['away']['idTeam'] = row['idTeam']
                dict[gameId]['away']['teamSlug'] = row['teamSlug']
                dict[gameId]['away']['logoURL'] = row['teamLogo']
            if row['marketName'] == 'Spread Betting':
                dict[gameId]['away']['spreadHandicap'] = row['currentHandicap']
                dict[gameId]['away']['spreadValue'] = row['value']
            if row['marketName'] == 'Moneyline':
                dict[gameId]['away']['moneyline'] = row['value']
            if row['marketName'] == 'Total Points Scored':
                dict[gameId]['away']['ouHandicap'] = row['currentHandicap']
                dict[gameId]['away']['ouValue'] = row['value']
        if row['hadvalue'] in ['H','U']:
            if row['hadvalue'] in ['H']:
                dict[gameId]['home']['team'] = row['selectionName']
                dict[gameId]['home']['idTeam'] = row['idTeam']
                dict[gameId]['home']['teamSlug'] = row['teamSlug']
                dict[gameId]['home']['logoURL'] = row['teamLogo']
            if row['marketName'] == 'Spread Betting':
                dict[gameId]['home']['spreadHandicap'] = row['currentHandicap']
                dict[gameId]['home']['spreadValue'] = row['value']
            if row['marketName'] == 'Moneyline':
                dict[gameId]['home']['moneyline'] = row['value']
            if row['marketName'] == 'Total Points Scored':
                dict[gameId]['home']['ouHandicap'] = row['currentHandicap']
                dict[gameId]['home']['ouValue'] = row['value']
    list = []
    for item in dict.values():
        list.append(item)
    return jsonify(data=list)
#    return jsonify(data=json.loads(df.to_json(orient="records")))

@app.route('/wagers/<gameId>', methods = ['GET'])
def get_user_fast_history(gameId):
    df = wagers_df[wagers_df['gameId'] == gameId]
    return json.dumps({'data':df.to_json(orient="records")})

@app.route('/team/<idTeam>/boxscores', methods = ['GET'])
def get_team_boxscores(idTeam):
    print(idTeam)
    idTeam = int(idTeam)
    # idTeam = '1610612765'
    team_details = team_lookup_df[team_lookup_df['idTeam'] == idTeam]
    df = boxscores_df[boxscores_df['idTeam'].isin(team_details['idTeam'])]
    df = df.sort_values(by=['idGame'],ascending=False)
    data = {
        "boxscores": json.loads(df.to_json(orient="records")),
        "team":json.loads(team_details.to_json(orient="records"))
    }
    return jsonify(data=data)

if __name__ == '__main__':
    app.run(debug=True)