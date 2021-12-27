import binance
from binance import enums
from termcolor import colored


class Orders:

    def __init__(self, client: binance.Client, symbol='BTCUSDT', test=True):
        print('Start Make Orders')

        self.client = client
        self.symbol = symbol
        self.coin = symbol[:-4]
        self.test = test
        self.symbol_info = self.get_symbol_info()
        self.buy_prices = []
        self.mean_price = 0
        self.quantity_buy = 0
        self.quantity_sell = 0
        self.last_price_buy = 0
        self.last_price_sell = 0
        self.quantity_balance = 0

        if self.test:
            print(colored('Start with test orders', 'blue'))
        else:
            print(colored('Save your money! Is real!', 'green'))

        print(f'Min Quantity to Order: {self.min_required()}')

    def get_balance(self):
        return self.client.get_account()

    def get_coin(self):
        return self.client.get_asset_balance(self.coin)

    def min_required(self):
        required = self.symbol_info['filters'][2]['minQty']
        return '{:.5f}'.format(float(required))

    def get_all_orders(self):
        return self.client.get_all_orders(symbol=self.symbol)

    def get_symbol_info(self):
        return self.client.get_symbol_info(self.symbol)

    def make_buy(self, price=None, pct=0.00005, pct_quantity=0.2):

        print(colored('Start Buy...', 'magenta'))

        price = price + price * pct
        price = '{:.5f}'.format(price)
        print(colored(f'Price to Buy: {price}', 'magenta'))

        quantity = '{:.5f}'.format(float(self.get_coin().get('free')) * pct_quantity)

        if quantity < self.min_required():
            quantity = self.min_required()

        print(colored(f'Quantity to Buy: {quantity}', 'magenta'))

        if self.test:
            order = self.client.create_test_order(
                symbol=self.symbol,
                side=self.client.SIDE_BUY,
                type=self.client.ORDER_TYPE_LIMIT,
                timeInForce=enums.TIME_IN_FORCE_GTC,
                quantity=100,
                price=price)

        else:
            order = self.client.create_order(
                symbol=self.symbol,
                side=self.client.SIDE_BUY,
                type=self.client.ORDER_TYPE_MARKET,
                quantity=quantity,
            )

        self.add_results(quantity, price, 'buy')

        print(colored('End Buy...', 'magenta'))
        return order

    def make_sell(self, price=None, pct=0.00009, pct_quantity=0.2):

        print(colored('Start Sell...', 'cyan'))

        price = price - price * pct
        price = '{:.5f}'.format(price)
        print(colored(f'Price to Sell: {price}', 'cyan'))

        quantity = '{:.5f}'.format(float(self.get_coin().get('free')) * pct_quantity)

        if quantity < self.min_required():
            quantity = self.min_required()

        print(colored(f'Quantity to Sell: {quantity}', 'cyan'))

        if self.test:
            order = self.client.create_test_order(
                symbol=self.symbol,
                side=self.client.SIDE_SELL,
                type=self.client.ORDER_TYPE_LIMIT,
                timeInForce=enums.TIME_IN_FORCE_GTC,
                quantity=100,
                price=price
            )

        else:
            order = self.client.create_order(
                symbol=self.symbol,
                side=self.client.SIDE_SELL,
                type=self.client.ORDER_TYPE_MARKET,
                quantity=quantity
            )

        self.add_results(quantity, price, 'sell')

        print(colored('End Sell...', 'cyan'))
        return order

    def add_results(self, quantity, price, action):

        if action == 'buy':
            self.quantity_buy += float(quantity)
            self.last_price_buy = price

        if action == 'sell':
            self.quantity_sell += float(quantity)
            self.last_price_sell = price

        self.quantity_balance = self.quantity_buy - self.quantity_sell

    def show_result(self):
        print(colored('**' * 10, 'yellow'))
        print(colored(f'Quantity Balance: {self.quantity_balance}', 'green'))
        print(colored(f'Quantity Sell: {self.quantity_sell}', 'green'))
        print(colored(f'Quantity Buy: {self.quantity_buy}', 'green'))
        print(colored(f'Last Price Sell: {self.last_price_sell}', 'green'))
        print(colored(f'Last Price Buy: {self.last_price_buy}', 'green'))
        print(colored('**' * 10, 'yellow'))
