import asyncio
import os
import signal

import jsonpickle
import numpy
import talib
import websockets
from talib import MA_Type
from trading.config.ftxconfig import client
from trading.repo import spotrepo
from trading.service import ftxservice
from trading.models import SpotMarket

from FTX.settings import ENV_FTX_WEBSOCKET_URI, ENV_FTX_WEBSOCKET_PING_INTERVAL
from trading.service.ftxwsservice import analyze_trade_market

loop = asyncio.new_event_loop()


def run():
    asyncio.run(analyze_trade_market('BTC/USD'))
    print('exited out')
    print(os.getppid())
    os.kill(os.getppid(), signal.CTRL_BREAK_EVENT)

    # points = client.get_klines('BTC/USD', 3600)
    # spot_markets = ftxservice.get_spot_markets()
    # for ftx_market in spot_markets:
    #     db_market = SpotMarket.from_ftx(ftx_market)
    #     print(db_market.name)
    #     db_market.save()

    # print(SpotMarket.objects.count())

    # close = numpy.array([point['close'] for point in points['result']])
    #
    # upper, middle, lower = talib.BBANDS(close, matype=MA_Type.T3, timeperiod=20)
    # print(type(upper[0]))
    # print(numpy.count_nonzero(numpy.isnan(upper)))
