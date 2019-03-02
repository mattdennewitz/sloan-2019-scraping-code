"""
Scrapes MLB's top 101 prospects list
"""

import csv

import requests

SYSTEM_ID = 'mlb'
URL = 'http://m.mlb.com/gen/players/prospects/2019/playerProspects.json'  # no https :'(


def scrape_mlb():
    """Extracts player data from BP
    """

    # we are scraping JSON here, not HTML - no special handlers required
    resp = requests.get(URL)
    resp.raise_for_status()  # do not continue if invalid

    # prepare csv writer
    writer = csv.DictWriter(
        open('prospects-mlb.csv', 'w'),
        fieldnames=(
            'system_id',
            'player_id',
            'rank',
            'player_name',
        ))
    writer.writeheader()

    # prospects are given an an array with name, rank, and id together
    mlb_prospect_body = resp.json()  # convert to json
    prospects = mlb_prospect_body['prospect_players']['prospects']

    for player in prospects:
        row = {
            'system_id':
            SYSTEM_ID,
            'player_id':
            player['player_id'],
            'rank':
            player['rank'],
            'player_name':
            '%s %s' % (player['player_first_name'], player['player_last_name'])
        }

        writer.writerow(row)


if __name__ == '__main__':
    scrape_mlb()
