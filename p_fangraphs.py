"""
Scrapes FanGraphs top 100 (132, really) prospects list
"""

import csv

from urllib import parse

from requests_html import HTMLSession

SYSTEM_ID = 'fg'
URL = 'https://blogs.fangraphs.com/2019-top-100-prospects/'


def scrape_fg():
    """Extracts player data from FG
    """

    # requests are made within a session
    session = HTMLSession()

    resp = session.get(URL)
    resp.raise_for_status()  # do not continue if invalid

    # prepare csv writer
    writer = csv.DictWriter(
        open('prospects-fg.csv', 'w'),
        fieldnames=(
            'system_id',
            'player_id',
            'rank',
            'player_name',
        ))
    writer.writeheader()

    # use xpath to find relevant table rows
    #
    # note: we know from inspecting the source that rows with TH elements
    #   are divider lines and should be ignored. we can find rows
    #   with td elements and back up to the row to select only
    #   the rows we want
    prospects_table = resp.html.xpath(
        '//div[contains(@class, "fullpostentry")]/'
        'div[contains(@class, "table-container")]/'
        'div[@class="table-wrapper"]/table[1]/tbody/tr/td/..')

    for player_row in prospects_table:
        # rank is from first TD
        rank = player_row.find('td', first=True).text

        # extract player name cell, and check for player link
        player_cell = player_row.find('td:nth-of-type(2)', first=True)
        player_link = player_cell.find('a', first=True)

        if player_link:
            url = player_link.attrs['href']

            # parse player id from url query string
            url_bits = parse.urlparse(url)
            qs_bits = parse.parse_qs(url_bits.query)
            player_id = qs_bits['playerid'][0]
            player_name = player_link.text.strip()
        else:  # fallback case for players without fg pages, hence no id
            player_id = None
            player_name = player_cell.text.strip()

        row = {
            'system_id': SYSTEM_ID,
            'player_id': player_id,
            'rank': rank,
            'player_name': player_name
        }

        writer.writerow(row)


if __name__ == '__main__':
    scrape_fg()
