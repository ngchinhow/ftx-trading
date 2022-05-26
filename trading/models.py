from __future__ import annotations

from datetime import datetime
from decimal import Decimal

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext as _

from trading.constants import FTX_SPOT_TRADE_TIME_FORMAT

NINEPLACES = Decimal(10) ** -9


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


class SpotTrade(models.Model):
    objects = models.Manager()

    id = models.DecimalField(max_digits=11, decimal_places=0, primary_key=True, db_column='Id')
    market = models.CharField(max_length=20, null=False, db_column='Market')
    price = models.DecimalField(max_digits=38, decimal_places=9, null=False, db_column='Price')
    size = models.DecimalField(max_digits=38, decimal_places=9, null=False, db_column='Size')
    side = models.CharField(max_length=4, db_column='Side')
    liquidation = models.BooleanField(db_column='Liquidation')
    time = models.DateTimeField(null=False, db_column='Time')

    @classmethod
    def from_ftx(cls, trade, market):
        st = cls()
        st.id = trade['id']
        st.market = market
        st.price = Decimal(trade['price'])
        st.size = Decimal(trade['size'])
        st.side = trade['side']
        st.liquidation = trade['liquidation']
        st.time = datetime.strptime(trade['time'], FTX_SPOT_TRADE_TIME_FORMAT)

        return st


@receiver(pre_save, sender=SpotTrade)
def spot_trade_pre_save(instance, **_kwargs):
    instance.price = instance.price.quantize(NINEPLACES)
    instance.size = instance.size.quantize(NINEPLACES)


class DataPoint(models.Model):
    objects = models.Manager()

    class DataPointType(models.TextChoices):
        RAW = 'RAW', _('Raw')
        RAW_SQUARED = 'RAW^2', _('Raw Squared')
        M1_EMA1 = 'M1EMA1', _('First Moment First Exponential Moving Average')
        M1_EMA2 = 'M1EMA2', _('First Moment Second Exponential Moving Average')
        M1_EMA3 = 'M1EMA3', _('First Moment Third Exponential Moving Average')
        M1_TEMA = 'M1TEMA', _('First Moment Triple Exponential Moving Average')
        M2_EMA1 = 'M2EMA1', _('Second Moment First Exponential Moving Average')
        M2_EMA2 = 'M2EMA2', _('Second Moment Second Exponential Moving Average')
        M2_EMA3 = 'M2EMA3', _('Second Moment Third Exponential Moving Average')
        M2_TEMA = 'M2TEMA', _('Second Moment Triple Exponential Moving Average')

    type = models.CharField(max_length=6, choices=DataPointType.choices, db_column='Type')
    value = models.DecimalField(max_digits=38, decimal_places=9, db_column='Value')
    time = models.DecimalField(max_digits=16, decimal_places=6, db_column='Time')


@receiver(pre_save, sender=DataPoint)
def data_point_pre_save(instance, **_kwargs):
    instance.value = instance.value.quantize(NINEPLACES)
