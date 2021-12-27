import pandas as pd
import numpy as np


def get_features(dataset: pd.DataFrame, max_min_list=None):
    if max_min_list is None:
        max_min_list = [5, 10, 20, 30, 60]

    dataset['Price'] = ((dataset['High'] + dataset['Low'] + dataset['Close']) / 3)
    dataset[f'diff_price'] = dataset['Price'].diff(1)
    dataset['sign'] = np.sign(dataset['diff_price'])

    for i in max_min_list:
        dataset[f'price_diff_{i}'] = dataset['Price'].diff(i)

        dataset[f'rolling_{i}'] = dataset.Close.rolling(window=i).mean()
        dataset[f'return_{i}'] = dataset.Close.diff(i)

        dataset[f'min_{i}'] = dataset.groupby([dataset.index // i])['Close'].transform('min')
        dataset[f'max_{i}'] = dataset.groupby([dataset.index // i])['Close'].transform('max')

        dataset[f'diff_{i}'] = abs(dataset.groupby([dataset.index // i])['diff_price'].transform('mean'))

        dataset[f'sell_{i}'] = dataset[f'max_{i}'] - dataset[f'diff_{i}']
        dataset[f'buy_{i}'] = dataset[f'min_{i}'] + dataset[f'diff_{i}']

        dataset[f'max_min_{i}'] = dataset[f'max_{i}'] - dataset[f'min_{i}']

        dataset[f'sign_{i}'] = np.sign(dataset.groupby([dataset.index // i])['sign'].transform('sum'))

    return dataset
