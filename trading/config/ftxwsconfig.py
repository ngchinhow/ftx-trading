import websockets

from FTX.settings import ENV_FTX_WEBSOCKET_URI, ENV_FTX_WEBSOCKET_PING_INTERVAL
from trading.dto.ftxwsdto import WebsocketSubscribeDTO, WebsocketSubscribedDTO


async def build_websocket(channel, market):
    subscribe_dto = WebsocketSubscribeDTO(channel, market)
    print(ENV_FTX_WEBSOCKET_PING_INTERVAL)
    websocket = await websockets.connect(ENV_FTX_WEBSOCKET_URI, ping_interval=ENV_FTX_WEBSOCKET_PING_INTERVAL)
    await websocket.send(subscribe_dto.to_json())
    response = await websocket.recv()
    subscribed_dto = WebsocketSubscribedDTO.from_json(response)

    # Assertions about websocket subscription
    assert subscribed_dto.type == 'subscribed'
    assert subscribed_dto.channel == channel
    assert subscribed_dto.market == market

    return websocket
