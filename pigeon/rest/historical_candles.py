from typing import Optional
from ..exceptions import BadResponse
import requests
from ..config import url_apis
from .authenticator import Authenticator
import json
import pandas as pd

class HistoricalCandles:
    """
    This class provides historical candles for a given ticker or all tickers available for query.

    * Main use case:

    >>> from pigeon import HistoricalCandles
    >>> hist_candles = HistoricalCandles(
    >>>     api_key='YOUR_API_KEY',
    >>> )
    >>> obj.get_historical_candles(
    >>>     ticker = 'PETR4',
    >>>     candle_period = '1M',
    >>>     mode = 'relative',
    >>>     benchmark = 'IBOV',
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
        api_key:Optional[str]
    ):
        self.api_key = api_key
        self.token = Authenticator(self.api_key).token
        self.headers = {"authorization": f"authorization {self.token}"}


    def get_historical_candles(
        self,
        ticker:str,
        period:str,
        mode:str,
        benchmark:str='',
        raw_data:bool=False
    ):
        """
        This method provides historical candles for a given ticket in determined period.

        Parameters
        ----------------
        ticker: str
            Ticker that needs to be returned.
            Field is required. Example: 'PETR4'.
        period: str
            Date period.
            Field is required. Example: '5D', '1M', '6M', 'YTD' or '1Y'.
        mode: str
            Candle mode.
            Field is required. Example: 'absolute' or 'relative'.
        benchmark: str
            Index benchmark.
            Field is not required. Default: '' (empty string).
        raw_data: bool
            If false, returns data in a dataframe. If true, returns raw data.
            Field is not required. Default: False.
        """     
        url = f"{url_apis}get_historical_candles?ticker={ticker}&period={period}&mode={mode}"
        if benchmark:
            url += f'&benchmark={benchmark}'

        response = requests.request("GET", url,  headers=self.headers)
        if response.status_code == 200:
            response_data = json.loads(response.text)
            if raw_data:
                return response_data
            elif not benchmark:
                return pd.DataFrame(response_data)
            else:
                df_ticker = pd.DataFrame(response_data.get('ticker'))
                df_benchmark = pd.DataFrame(response_data.get('benchmark'))
                df_benchmark = df_benchmark.rename(columns=lambda x: f'{x}_benchmark')
                return pd.merge(df_ticker, df_benchmark, left_on='date', right_on='date_benchmark')

        else:
            response = json.loads(response.text)
            raise BadResponse(f'Error: {response.get("ApiClientError")}.\n{response.get("SuggestedAction")}')

    def get_available_tickers(self):  
        """
        This method provides all tickers available for query.   
        """
        url = f"{url_apis}get_historical_candles/available_tickers"
        response = requests.request("GET", url,  headers=self.headers)

        if response.status_code == 200:
            return json.loads(response.text).get('available_tickers', [])
        else:
            response = json.loads(response.text)
            raise BadResponse(f'Error: {response.get("ApiClientError")}.\n{response.get("SuggestedAction")}')