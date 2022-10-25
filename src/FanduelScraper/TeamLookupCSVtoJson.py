##############################
## Team Lookup CSV to JSON
##############################
import csv

slug_data = {}
id_data = {}
with open('NBA/team_lookup.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        print(row['teamSlug'])
        record = {
            'nbaIdTeam': row['idTeam'],
            'fanduelName': row['fanduel_name'],
            'boxscoreName': row['boxscore_name'],
            'teamSlug': row['teamSlug'],
            'teamLogoUrl': row['teamLogo'],
            'teamLogoPathSVG':row['teamLogoPathSVG'],
            'teamLogoPathPNG': row['teamLogoPathPNG']
        }
        slug_data[row['teamSlug']] = record
        id_data[row['idTeam']] = record
    line_count += 1

import json
with open('NBA/team_lookup_slug.json', 'w') as outfile:
    json.dump(slug_data, outfile)

with open('NBA/team_lookup_id.json', 'w') as outfile:
    json.dump(id_data, outfile)

##############################
## Player Prop History Df to JSON
##############################
