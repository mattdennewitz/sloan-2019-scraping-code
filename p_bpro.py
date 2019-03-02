"""
Scrapes Baseball Prospectus top 101 prospects list
"""

import csv

from urllib import parse

from requests_html import HTMLSession

SYSTEM_ID = 'bp'
URL = 'https://www.baseballprospectus.com/news/article/46653/2019-prospects-the-top-101/'
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0'


def scrape_bp():
    """Extracts player data from BP
    """

    # requests are made within a session
    session = HTMLSession()

    # BP has bot detection that will reject non-standard requests.
    # to get around this edge case, we masquerade as a regular browser
    # by sending a common browser identification string in the
    # User-Agent HTTP header. without this, the request will be denied.
    resp = session.get(
        URL,
        headers={
            'user-agent': USER_AGENT,  # set user-agent header
        })
    resp.raise_for_status()  # do not continue if invalid

    # prepare csv writer
    writer = csv.DictWriter(
        open('prospects-bp.csv', 'w'),
        fieldnames=(
            'system_id',
            'player_id',
            'rank',
            'player_name',
        ))
    writer.writeheader()

    # use css to find prospect list, an OL and the only on the page.
    # each player is stored in a `span.playerdef` wrapper.
    #
    # note: we know from inspecting the source that each prospect exists
    #   in an ordered list. from this we must infer ordering. we also know
    #   that each prospect has a link, but only player card links have ids.
    prospects = resp.html.find(
        'section.content.article.article-detail article ol .playerdef a')

    for rank_idx, player_link in enumerate(prospects):
        rank = rank_idx + 1  # infer rank from order in list

        url = player_link.attrs['href']
        player_name = player_link.text.strip()

        if 'card.php' in url:
            # parse player id from url query string
            url_bits = parse.urlparse(url)
            qs_bits = parse.parse_qs(url_bits.query)
            player_id = qs_bits['id'][0]
        else:
            player_id = None

        row = {
            'system_id': SYSTEM_ID,
            'player_id': player_id,
            'rank': rank,
            'player_name': player_name
        }

        writer.writerow(row)


if __name__ == '__main__':
    scrape_bp()
