from trading.config.ftxconfig import client
from trading.models import SpotMarket
from trading.repo.djangorepo import bulk_create_spot_markets


def get_spot_markets():
    return filter(
        lambda m: m['type'] == 'spot' and not m['isEtfMarket'],
        client.get_markets()['result']
    )


def save_spot_markets():
    markets = []
    spot_markets = get_spot_markets()
    for ftx_market in spot_markets:
        db_market = SpotMarket.from_ftx(ftx_market)
        markets.append(db_market)

    return bulk_create_spot_markets(markets)
