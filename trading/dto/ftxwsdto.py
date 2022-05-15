import json


class WebsocketSubscribeDTO:
    def __init__(self, channel, market):
        self.op = 'subscribe'
        self.channel = channel
        self.market = market

    def to_json(self):
        return json.dumps(vars(self))


class WebsocketSubscribedDTO:
    def __init__(self, action_type, channel, market):
        self.type = action_type
        self.channel = channel
        self.market = market

    @classmethod
    def from_json(cls, response_str):
        response_dict = json.loads(response_str)
        print(response_dict)
        return cls(response_dict['type'], response_dict['channel'], response_dict['market'])


class WebSocketResponseDTO:
    def __init__(self, **kwargs):
        allowed_keys = {'channel', 'market', 'type', 'code', 'msg', 'data'}
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)


class WebSocketTradeResponseDTO(WebSocketResponseDTO):
    def __init__(self, kwargs):
        super().__init__(kwargs)

    class TradeDataDTO:
        def __init__(self, data_id, price, size, side, liquidation, time):
            self.id = data_id
            self.price = price
            self.size = size
            self.side = side
            self.liquidation = liquidation
            self.time = time

        @classmethod
        def from_dict(cls, response_dict):
            return cls(
                response_dict['id'],
                response_dict['price'],
                response_dict['size'],
                response_dict['side'],
                response_dict['liquidation'],
                response_dict['time']
            )

    def from_json(self, response_str):
        response_dict = json.loads(response_str)
        if 'data' in response_dict:
            response_dict['data'] = [self.TradeDataDTO.from_dict(point) for point in response_dict['data']]
