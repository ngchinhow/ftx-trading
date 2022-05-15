from trading.config.ftxconfig import client


def get_spot_markets():
    return filter(
        lambda m: m['type'] == 'spot' and not m['isEtfMarket'],
        client.get_markets()['result']
    )
