import datetime
import os
import pandas as pd
import numpy as np
import yfinance as yf

from .util import *

now = datetime.datetime.now()

DATE = 0
OPEN = 1
ADJ_CLOSE = 5

def download(tickers):
    all_data = {}

    for key, val in tickers.items():
        print(f"Downloading {key}, {val} data...")
        data = yf.download(val, start='1994-01-01', interval='1wk', progress=False)
        data.index = data.index.strftime("%Y%m%d").astype(int)
        all_data[key] = data

    return all_data

def to_monthly_data(data):
    monthly_data = {}
    for key, val in data.items():
        val.index = pd.to_datetime(val.index, format='%Y%m%d')
        monthly_data[key] = val.resample('M').first()
        monthly_data[key].index = monthly_data[key].index.strftime("%Y%m%d").astype(int)

    return monthly_data

def clean_data(data):
    cleaned_data = {}

    for sector, df in data.items():
        df = df.loc[:, ["Open", "Adj Close"]]

        if sector == "T_BILL_3_MO":
            cleaned_data[sector] = remove_unnecessary_data(df, True)
        else:
            cleaned_data[sector] = remove_unnecessary_data(df)

    return cleaned_data

def remove_unnecessary_data(data, t_bill=False):
    if (t_bill):
        data['Return'] = data['Adj Close'] / 100
        return data.loc[:, 'Return']
    else:
        data['Return'] = (data['Adj Close'] - data['Open']) / data['Open']
        return data.loc[:, 'Return']