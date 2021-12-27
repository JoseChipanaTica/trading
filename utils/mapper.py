import pandas as pd


def hlc_to_frame(item: list, symbol='BTCUSDT'):
    frame = pd.DataFrame(item, columns=[
        'OpenTime',
        'Open',
        'High',
        'Low',
        'Close',
        'Volume',
        'CloseTime',
        'QuoteAssetVolume',
        'NumberTraders',
        'TakerBuyBase',
        'TakerBuyQuote',
        'Ignore'
    ])

    frame['Open'] = frame['Open'].astype('float64')
    frame['High'] = frame['High'].astype('float64')
    frame['Low'] = frame['Low'].astype('float64')
    frame['Close'] = frame['Close'].astype('float64')
    frame['Volume'] = frame['Volume'].astype('float64')

    frame['symbol'] = symbol
    frame['OpenTime'] = pd.to_datetime(frame['OpenTime'] / 1000, unit='s')

    frame = frame[-60:]
    return frame
