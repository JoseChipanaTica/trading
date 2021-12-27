from controller import historical, orders
from config import connection
from utils import mapper, graphics
from features import features_coins
from prefect import task, Flow
from prefect.schedules import IntervalSchedule
from datetime import timedelta
from utils import utils
from termcolor import colored


class Coins:

    def __init__(self, symbol, time='10', test=True):

        self.symbol = symbol
        self.time = time
        self.test = test
        print(colored(self.symbol, 'green'))

        self.data = historical.GetData(connection.client)
        self.order = orders.Orders(connection.client, self.symbol, test=self.test)

    @task()
    def extract(self):
        items = self.data.get_current(self.symbol, minutes=60)
        frame = mapper.hlc_to_frame(items, self.symbol)
        df_features = features_coins.get_features(frame)

        last = frame[-1:]
        last_features = df_features[-2:]

        last_open_time = last.OpenTime.values[0]
        last_sell = last_features[f'sell_{self.time}'].values[0]
        last_buy = last_features[f'buy_{self.time}'].values[0]
        last_close = last.Close.values[0]
        last_trend = last_features[f'sign_{self.time}'].values[0]

        graphics.candelstick_chart(df_features, 'Last Hour')
        graphics.show_max_min(df_features, time=self.time)
        graphics.show_diff(df_features, f'diff_price')

        print(colored(f'Time: {last_open_time}', 'grey'))
        print(colored(f'Last Sell: {last_sell}', 'grey'))
        print(colored(f'Close: {last_close}', 'grey'))
        print(colored(f'Last Buy: {last_buy}', 'grey'))

        diff, action = utils.search_near(last_close, last_sell, last_buy)

        try:
            if last_trend == 1:
                print(colored('Trend Positive', 'yellow'))
            elif last_trend == 0:
                print(colored('No trend', 'yellow'))
            else:
                print(colored('Trend Negative', 'yellow'))

            if last_close >= last_sell:
                print(colored('Time to sell', 'cyan'))
                self.order.make_sell(last_sell)
            else:
                print(colored('Bad time to sell', 'red'))

            if last_close <= last_buy:
                print(colored('Time to Buy', 'magenta'))
                self.order.make_buy(last_buy)
            else:
                print(colored('Bad time to buy', 'red'))

            # if diff < diff_apl:
            #     print('Is near To...')
            #     if action == 'buy':
            #         order.make_buy(last_buy)
            #     if action == 'sell':
            #         order.make_sell(last_sell)

        except ():
            print('Error...')

        return ''

    @task()
    def show_balance(self):
        self.order.show_result()
        return ''

    def build_flow(self):
        schedule = IntervalSchedule(interval=timedelta(minutes=1))

        with Flow('Coins', schedule) as _flow:
            _ = self.extract(self)
            _ = self.show_balance(self)

        return _flow
