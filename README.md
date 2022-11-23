# Pigeon

Pigeon is a Python library to get Brazilian Financial Market Data.

## Installation

```bash
pip3 install pigeonapi-python-client
```

## Example - WebSocket

```python
import pigeon

ws = pigeon.WebSocketClient(api_key='YOUR_API_KEY', instruments=['PETR4', 'VALE3'])
ws.run(on_message=lambda message: print(message))
```
## Example - IntradayCandles

```python
import pigeon

int_candles = pigeon.IntradayCandles(api_key='YOUR_API_KEY')
int_candles.get_intraday_candles(ticker='PETR4', candle_period='1m', mode='relative')
```
## Example - HistoricalCandles

```python
import  pigeon

hist_candles = pigeon.HistoricalCandles(api_key='YOUR_API_KEY')
hist_candles.get_historical_candles(ticker='PETR4', period='5D', mode='relative').plot(x='date', y='close_price', kind='scatter')
```