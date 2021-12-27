import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def candelstick_chart(data: pd.DataFrame, title: str):
    candlestick = go.Figure(data=[go.Candlestick(x=data['OpenTime'],
                                                 open=data['Open'],
                                                 high=data['High'],
                                                 low=data['Low'],
                                                 close=data['Close'])])

    candlestick.update_layout(
        title={
            'text': '{:} Candelstick Chart'.format(title),
            'y': 0.90,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    candlestick.update_yaxes(title_text='Price in USD', ticksuffix='$')
    candlestick.show()


def show_max_min(dataset: pd.DataFrame, show_min_max=False, show_buy_sell=True, time='10'):
    y = ['Close', 'Open', 'High', 'Low']

    if show_min_max:
        y.extend([
            'min_5', 'max_5',
            'min_10', 'max_10',
            'min_20', 'max_20',
            'min_30', 'max_30'])

    if show_buy_sell:
        if time == '5':
            y.extend(['sell_5', 'buy_5'])
        if time == '10':
            y.extend(['sell_10', 'buy_10'])
        if time == '20':
            y.extend(['sell_20', 'buy_20'])
        if time == '30':
            y.extend(['sell_30', 'buy_30'])

    px.line(dataset, x='OpenTime', y=y).show()


def show_diff(dataset: pd.DataFrame, col):
    fig = px.line(dataset, x='OpenTime', y=col).show()

