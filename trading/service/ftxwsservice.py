import asyncio
import threading
import websockets
import FTX
from FTX.settings import STOP_EVENT
from trading.config.ftxwsconfig import build_websocket


async def analyze_trade_market(market):
    FTX.settings.WEBSOCKET_THREAD = threading.current_thread()
    ws = await build_websocket('trades', market)
    try:
        async for message in ws:
            if STOP_EVENT.is_set():
                await ws.close()
                print('socket closed successfully')
            print(message)
    except websockets.ConnectionClosed:
        print('closed')
