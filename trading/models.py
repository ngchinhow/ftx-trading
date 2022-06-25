from __future__ import annotations
from django.db import models

from trading.constants import FTX_SPOT_TRADE_TIME_FORMAT


class SpotMarket(models.Model):
    # Explicitly exposing manager so that the IDE doesn't complain
    objects = models.Manager()

    name = models.CharField(max_length=20, primary_key=True, db_column='SpotName')
    enabled = models.BooleanField(db_column='Enabled')
    price_increment = models.DecimalField(max_digits=13, decimal_places=9, db_column='PriceIncrement')
    size_increment = models.DecimalField(max_digits=13, decimal_places=6, db_column='SizeIncrement')
    # Minimum maker order size( if > 10 orders per hour fall below this size)
    min_provide_size = models.DecimalField(max_digits=13, decimal_places=6, db_column='MinProvideSize')
    is_etf_market = models.BooleanField(db_column='IsETFMarket')
    base_currency = models.CharField(max_length=10, db_column='BaseCurrency')
    quote_currency = models.CharField(max_length=10, db_column='QuoteCurrency')
    # threshold above which an order is considered large(for VIP rate limits)
    large_order_threshold = models.DecimalField(max_digits=10, decimal_places=5, db_column='LargeOrderThreshold')

    @classmethod
    def from_ftx(cls, market: dict) -> SpotMarket:
        sm = cls()
        sm.name = market['name']
        sm.enabled = market['enabled']
        sm.price_increment = market['priceIncrement']
        sm.size_increment = market['sizeIncrement']
        sm.min_provide_size = market['minProvideSize']
        sm.is_etf_market = market['isEtfMarket']
        sm.base_currency = market['baseCurrency']
        sm.quote_currency = market['quoteCurrency']
        sm.large_order_threshold = market['largeOrderThreshold']

        return sm


class CandleStick(models.Model):
    objects = models.Manager()

    market = models.CharField(max_length=20, null=False, db_column='Market')
    high = models.DecimalField(max_digits=38, decimal_places=28, db_column='High')
    low = models.DecimalField(max_digits=38, decimal_places=28, db_column='Low')
    average = models.DecimalField(max_digits=38, decimal_places=28, db_column='Average')
    ema_20 = models.DecimalField(max_digits=38, decimal_places=28, db_column='EMA20')
    ema_50 = models.DecimalField(max_digits=38, decimal_places=28, db_column='EMA50')
    ema_200 = models.DecimalField(max_digits=38, decimal_places=28, db_column='EMA200')
    bb_plus = models.DecimalField(max_digits=38, decimal_places=28, db_column='UpperBollingerBand')
    bb_minus = models.DecimalField(max_digits=38, decimal_places=28, db_column='LowerBollingerBand')
    rsi = models.DecimalField(max_digits=38, decimal_places=28, db_column='RelativeStrengthIndex')
    time = models.DateTimeField(null=False, db_column='Time')
