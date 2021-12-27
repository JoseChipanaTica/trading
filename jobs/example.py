from controller import historical, orders
from config import connection

symbol = 'GALAUSDT'

data = connection.client.futures_klines(symbol=symbol, interval=connection.client.KLINE_INTERVAL_5MINUTE)
