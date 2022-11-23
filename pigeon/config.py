### WebSocket 
socket_urls = {
    'derivatives_realtime': {
        'trades': "wss://websockets.pigeonapi.io/v2/marketdata/trade/derivatives",
        'books': "wss://websockets.pigeonapi.io/v2/marketdata/book/derivatives",
    },
    # 'derivatives_delayed': {
    #     'trades': "wss://websockets.pigeonapi.io/v2/marketdata/trade/derivatives/delayed",
    #     'books': "wss://websockets.pigeonapi.io/v2/marketdata/book/derivatives/delayed",
    # },
    'stocks_realtime': {
        'trades': "wss://websockets.pigeonapi.io/v2/marketdata/trade/stocks",
        'books': "wss://websockets.pigeonapi.io/v2/marketdata/book/stocks",
    },
    # 'stocks_delayed': {
    #     'trades': "wss://websockets.pigeonapi.io/v2/marketdata/trade/stocks/delayed",
    #     'books': "wss://websockets.pigeonapi.io/v2/marketdata/book/stocks/delayed",
    # },
    'options_realtime': {
        'trades': "wss://websockets.pigeonapi.io/v2/marketdata/trade/options",
        'books': "wss://websockets.pigeonapi.io/v2/marketdata/book/options",
    },
    # 'options_delayed': {
    #     'trades': "wss://websockets.pigeonapi.io/v2/marketdata/trade/options/delayed",
    #     'books': "wss://websockets.pigeonapi.io/v2/marketdata/book/options/delayed",
    # },
    'indices_realtime': "wss://websockets.pigeonapi.io/v2/marketdata/indices",
    # 'indices_delayed': "wss://websockets.pigeonapi.io/v2/marketdata/indices/delayed"
}

keys_socket = list(socket_urls.keys())

valid_delayed_options = list(set([i.split('_')[1] for i in keys_socket]))
valid_feeds = list(set([i.split('_')[0] for i in keys_socket]))

def valid_ws_options(feed, target):
    return list(set(socket_urls[f'{feed}_{target}']))


### Rest
url_apis = "https://gofast.btgpactualsolutions.com/api/v1.1/"