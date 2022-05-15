from trading.models import SpotMarket


def get_spot_markets():
    return SpotMarket.objects.all()


def bulk_create_spot_markets(markets):
    return SpotMarket.objects.bulk_create(markets)


def bulk_update_spot_markets(markets) -> int:
    return SpotMarket.objects.bulk_update(markets)
