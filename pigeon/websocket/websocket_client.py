
from typing import Optional, List
from ..exceptions import WSTypeError, DelayedError, FeedError
from ..rest import Authenticator
from ..config import valid_feeds, valid_ws_options, valid_delayed_options, socket_urls
from .websocket_default_functions import _on_open, _on_message, _on_error, _on_close
import websocket 
import json
import threading
 
class WebSocketClient:
    """
    This class connects with Pigeon WebSocket, receiving trade and index data, in real time or delayed.

    * Main use case:

    >>> from pigeon import WebSocketClient
    >>> ws = WebSocketClient(
    >>>     api_key='YOUR_API_KEY',
    >>>     feed='stocks',
    >>>     target='realtime',
    >>>     ws_type='trades',
    >>>     instruments=['PETR4']
    >>> )
    >>> ws.run()
    >>> ws.subscribe(['MGLU3'])
    >>> ws.unsubscribe(['PETR4'])
    >>> ws.close()

    Parameters
    ----------------
    api_key: str
        User identification key.
        Field is required.

    feed: str
        Websocket connection feed.
        Options: 'stocks', 'options', 'derivatives' or 'indices'
        Field is not required. Default: 'stocks'.

    target: str
        Data update type.
        Options: 'realtime' or 'delayed'.
        Field is not required. Default: 'realtime'.

    ws_type: str
        Connection type with WebSocketClient.
        Options: 'trades' or 'book'.
        If the feed is 'indices' this field is not used.
        Field is not required. Default: 'trades'.

    instruments: list
        List of tickers or indexes to subscribe.
        Field is not required. Default: [].

    """
    def __init__(
        self,
        api_key:str,
        feed:Optional[str] = 'stocks',
        target:Optional[str] = 'realtime',
        ws_type:Optional[str] = 'trade',
        instruments:Optional[List[str]] = [],
        **kwargs,
    ):
        self.api_key = api_key
        self.token = Authenticator(self.api_key).token
        self.protocol_str = {"Sec-WebSocket-Protocol": self.token}
        self.instruments = instruments
        if feed not in valid_feeds:
            raise FeedError(
                f"Must provide a valid 'feed' parameter. Valid options are: {valid_feeds}"
            )
        if target not in valid_delayed_options:
            raise DelayedError(
                f"Must provide a valid 'target' parameter. Valid options are: {valid_delayed_options}"
            )
        
        if feed != 'indice':
            if ws_type not in valid_ws_options(feed, target):
                raise WSTypeError(
                    f"Must provide a valid 'ws_type' parameter. Valid options are: {valid_ws_options(feed, target)}"
                )
            self.url = socket_urls[f'{feed}_{target}'][ws_type]
        else:
            self.url = socket_urls[f'{feed}_{target}']
            
        self.websocket_cfg = kwargs
    
    def run(
        self,
        on_open = None,
        on_message = None,
        on_error = None,
        on_close = None,
    ):
        """
        Initializes a connection to Pigeon WebSocket and subscribes to the instruments, if it was passed in the class initialization.

        Parameters
        ----------
        on_open: function
            - Called at opening connection to Pigeon WebSocket.
            - Arguments: None.
            - Field is not required. 
            - Default: prints that the connection was opened in case of success.
        
        on_message: function
            - Called every time it receives a message.
            - Arguments:
                1. Data received from the server.
            - Field is not required. 
            - Default: prints the data.

        on_error: function
            Called when a error occurs.
            Arguments: 
                1. Exception object.
            Field is not required. 
            Default: prints the error.

        on_close: function
            Called when connection is closed.
            Arguments: 
                1. close_status_code.
                2. close_msg.
            Field is not required. 
            Default: prints a message that the connection was closed.
        """
        if on_open is None:
            on_open = _on_open
        if on_message is None:
            on_message = _on_message
        if on_error is None:
            on_error = _on_error
        if on_close is None:
            on_close = _on_close

        def intermediary_on_open(ws):
            on_open()
            if self.instruments:
                self.subscribe(self.instruments)

        def intermediary_on_message(ws, data):
            on_message(data)

        def intermediary_on_error(ws, error):
            on_error(error)

        def intermediary_on_close(ws, close_status_code, close_msg):
            on_close(close_status_code, close_msg)

        self.ws = websocket.WebSocketApp(
            url=self.url,
            on_open=intermediary_on_open,
            on_message=intermediary_on_message,
            on_error=intermediary_on_error,
            on_close=intermediary_on_close, 
            header=self.protocol_str
        )

        wst = threading.Thread(target=self.ws.run_forever)
        wst.daemon = True
        wst.start()

    def __send(self, data):
        """
        Class method to be used internally. Sends data to the Pigeon WebSocket.
        """
        if not isinstance(data, str):
            data = json.dumps(data)   
        print(f'Sending data: {data}')
        return self.ws.send(data)
    
    def close(self):
        """
        Closes connection with Pigeon WebSocket.
        """
        self.ws.close()

    def subscribe(self, list_instruments):
        """
        Subscribes a list of instruments.

        Parameters
        ----------
        list_instruments: list
            Field is required.
        """
        self.__send({'action':'subscribe', 'params': list_instruments})
        print(f'Socket subscribed the following instrument(s): {list_instruments}')

    def unsubscribe(self, list_instruments):
        """
        Unsubscribes a list of instruments.

        Parameters
        ----------
        list_instruments: list
            Field is required.
        """
        self.__send({'action':'unsubscribe', 'params': list_instruments})
        print(f'Socket subscribed the following instrument(s): {list_instruments}')