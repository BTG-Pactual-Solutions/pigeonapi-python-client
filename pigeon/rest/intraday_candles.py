
from typing import Optional
from ..exceptions import BadResponse
import requests
from ..config import url_apis
import json
import pandas as pd
from .authenticator import Authenticator

class IntradayCandles:
    """
    This class provides realtime intraday candles for a given ticker or all tickers available for query.

    * Main use case:

    >>> from pigeon import IntradayCandles
    >>> hist_candles = IntradayCandles(
    >>>     api_key='YOUR_API_KEY',
    >>> )
    >>> obj.get_intraday_candles(
    >>>     ticker = 'PETR4',
    >>>     candle_period = '1m',
    >>>     mode = 'relative',
    >>>     raw_data = False
    >>> )

    Parameters
    ----------------
    api_key: str
        User identification key.
        Field is required.
    """
    def __init__(
        self,
        api_key: Optional[str]
    ):
        self.api_key = api_key
        self.token = Authenticator(self.api_key).token
        self.headers = {"authorization": f"authorization {self.token}"}

    def get_intraday_candles(
        self,
        ticker:str,
        candle_period:str,
        mode:str,
        raw_data:bool=False
    ):     
        """
        This method provides realtime intraday candles for a given ticker.

        Parameters
        ----------------
        ticker: str
            Ticker that needs to be returned.
            Field is required. Example: 'PETR4'.
        period: str
            Date period.
            Field is required. Examples: '1m'.
        mode: str
            Candle mode.
            Field is required. Example: 'absolute' or 'relative'.
        raw_data: bool
            If false, returns data in a dataframe. If true, returns raw data.
            Field is not required. Default: False.
        """
        url = f"{url_apis}get_candles_intraday?ticker={ticker}&candle_period={candle_period}&mode={mode}"
        response = requests.request("GET", url,  headers=self.headers)
        if response.status_code == 200:
            response_data = json.loads(response.text)
            return response_data if raw_data else pd.DataFrame(response_data)
        else:
            response = json.loads(response.text)
            raise BadResponse(f'Error: {response.get("ApiClientError")}.\n{response.get("SuggestedAction")}')

    def get_available_tickers(self):
        """
        This method provides all tickers available for query.   
        """
        url = f"{url_apis}get_candles_intraday/available_tickers"
        response = requests.request("GET", url,  headers=self.headers)
        if response.status_code == 200:
            return json.loads(response.text).get('available_tickers', [])
        else:
            response = json.loads(response.text)
            raise BadResponse(f'Error: {response.get("ApiClientError")}.\n{response.get("SuggestedAction")}')