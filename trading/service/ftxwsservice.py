import json
import threading
import datetime
from zoneinfo import ZoneInfo

import websockets

import FTX.settings

from decimal import Decimal
from asgiref.sync import sync_to_async, async_to_sync
from trading.config.ftxwsconfig import build_websocket
from trading.constants import FTX_SPOT_TRADE_TIME_FORMAT
from trading.models import CandleStick
from trading.repo.djangorepo import bulk_create_candle_sticks
from trading.service.indicator_calculator import do_ema, do_rsi, do_bbands

BATCH_SIZE = 100
CANDLE_STICKS = [CandleStick()] * BATCH_SIZE


@async_to_sync
async def analyze_trade_market(market: str):
    """
    Listens to, collates, calculates and stores trading data provided by FTX for a particular market.

    value indices
    -----------
    0: raw
    1: ema_raw_20
    2: ema_raw_20_variance
    3: ema_raw_50
    4: ema_raw_200
    5: up
    6: down
    7: ema_up_14
    8: ema_down_14
    """

    def initialize_values():
        return Decimal(0), 0, 0, 10 ** 9

    def do_frame_calculations(average, index):
        up, down = (diff, 0) if (diff := average - values[index - 1][0]) > 0 else (0, -diff)
        ema_20, ema_20_var = do_ema(average, values[index - 1][1], values[index - 1][2], alpha_20)

        return (
            average,
            ema_20,
            ema_20_var,
            do_ema(average, values[index - 1][3], 0, alpha_50)[0],
            do_ema(average, values[index - 1][4], 0, alpha_200)[0],
            up,
            down,
            do_ema(up, values[index - 1][7], 0, alpha_14)[0],
            do_ema(down, values[index - 1][8], 0, alpha_14)[0]
        )

    def assign_calculations(time, index):
        values[index] = calculations
        bb_plus, bb_minus = do_bbands(calculations[1], calculations[2])

        CANDLE_STICKS[index] = CandleStick(
            market=market,
            high=high,
            low=low,
            average=calculations[0],
            ema_20=calculations[1],
            ema_50=calculations[3],
            ema_200=calculations[4],
            bb_plus=bb_plus,
            bb_minus=bb_minus,
            rsi=do_rsi(calculations[7], calculations[8]),
            time=time
        )

    FTX.settings.WEBSOCKET_THREAD = threading.current_thread()

    window_length = 2
    values = [(Decimal(0.0001),) * 9 for i in range(BATCH_SIZE)]
    j = 0
    value_sum, value_counter, high, low = initialize_values()
    alpha_14 = Decimal(2 / (14 + 1))
    alpha_20 = Decimal(2 / (20 + 1))
    alpha_50 = Decimal(2 / (50 + 1))
    alpha_200 = Decimal(2 / (200 + 1))
    ws = await build_websocket('trades', market)

    try:
        current_time = local_time()
        async for message in ws:
            if FTX.settings.STOP_EVENT.is_set():
                await ws.close()
                print('socket closed successfully')

            message_dict = json.loads(message)
            for trade in message_dict['data']:
                if (trade_time := datetime.datetime.strptime(trade['time'], FTX_SPOT_TRADE_TIME_FORMAT)) < \
                        local_time() - datetime.timedelta(seconds=window_length):
                    window_length *= 2
                    print('window expanded to ', window_length)

                if trade_time >= (next_time := current_time + datetime.timedelta(seconds=window_length)):
                    calculations = do_frame_calculations(value_sum / value_counter, j)
                    if j == BATCH_SIZE:
                        await save_candle_sticks()
                        j = 0
                    assign_calculations(next_time, j)
                    current_time = next_time
                    value_sum, value_counter, high, low = initialize_values()
                    j += 1

                value = Decimal(trade['price']) * Decimal(trade['size'])
                if value > high:
                    high = value

                if value < low:
                    low = value

                value_sum += value
                value_counter += 1
    except websockets.ConnectionClosed:
        print('closed')


@sync_to_async
def save_candle_sticks():
    bulk_create_candle_sticks(CANDLE_STICKS)
    print('batch saved')


def local_time():
    return datetime.datetime.now(ZoneInfo('Asia/Singapore'))
