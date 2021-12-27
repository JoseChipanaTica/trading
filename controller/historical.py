import binance
from datetime import datetime
from datetime import timedelta


class GetData:

    def __init__(self, client: binance.Client):
        self.client = client
        self.interval = client.KLINE_INTERVAL_1MINUTE
        self.start_date = datetime(2021, 10, 31, 0, 0)
        self.end_date = datetime(2021, 11, 26, 0, 0)
        self.last_current = datetime.now() - timedelta(minutes=30)

    def get_coins_list(self):
        return self.client.get_all_tickers()

    def get_daily_by_symbol(self, symbol='BTCUSDT'):
        start_str = self.start_date.strftime('%d %b, %Y')
        end_str = self.end_date.strftime('%d %b, %Y')

        print(start_str)
        print(end_str)

        items = self.client.get_historical_klines(symbol, self.interval, start_str, end_str)

        return items

    def get_current(self, symbol='BTCUSDT', minutes=10):
        self.last_current = datetime.now() - timedelta(minutes=minutes)
        start_str = int(self.last_current.timestamp()) * 1000
        items = self.client.get_historical_klines(symbol, self.interval, start_str)

        return items
