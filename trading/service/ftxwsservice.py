import json
import threading
import websockets
from asgiref.sync import sync_to_async, async_to_sync
from django.db import IntegrityError

import FTX
from FTX.settings import STOP_EVENT
from trading.config.ftxwsconfig import build_websocket
from trading.models import SpotTrade


@async_to_sync
async def analyze_trade_market(market):
    FTX.settings.WEBSOCKET_THREAD = threading.current_thread()
    ws = await build_websocket('trades', market)
    try:
        async for message in ws:
            if STOP_EVENT.is_set():
                await ws.close()
                print('socket closed successfully')

            message_dict = json.loads(message)
            for trade in message_dict['data']:
                st = SpotTrade.from_ftx(trade, message_dict['market'])
                print(st.id)
                print(st.price)
                print(st.size)
                print(st.time)
                await save_data_points(st)
    except websockets.ConnectionClosed:
        print('closed')


@sync_to_async
def save_data_points(data_point):
    try:
        data_point.save()
    except IntegrityError:
        print('Uniqueness violated by ' + data_point.id + ' ' + data_point.time)
