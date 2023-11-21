import datetime
import os
import pandas as pd
import numpy as np
import yfinance as yf

from util import update, read_data, percentage_change


tickers = {
    "T_BILL_3_MO": "^IRX",
    "SP_FINANCE": "^SP500-40",
    "SP_ENEGY": "^GSPE",
    "SP_MATERIALS": "^SP500-15",
    "SP_CONSUM_DIS": "^SP500-25",
    "SP_CONSUM_STAPLE": "^SP500-30",
    "SP_HEALTH": "^SP500-35",
    "SP_UTIL": "^SP500-55",
    "SP_500": "^GSPC",
    "SP_INFO_TECH": "^SP500-45",
    "SP_TELE_COMM": "^SP500-50"
}

now = datetime.datetime.now()

DATE = 0
OPEN = 1
ADJ_CLOSE = 5

LAST_UPDATE_PATH = os.path.join("./data/last_update.txt")
EXPORT_PATH = os.path.join("./data")

def download():
    all_data = {}

    for key, val in tickers.items():
        data = yf.download(val, start='1994-01-01')
        all_data[key] = data

    return all_data

def to_monthly_data(data):
    monthly_data = {}
    for key, val in data.items():
        val.index = pd.to_datetime(val.index, format="%Y%m%d")
        monthly_data[key] = val.resample("M").last()

    return monthly_data

def clean_data(data):
    cleaned_data = {}

    for sector, df in data.items():
        df = df.reset_index()
        df[df.columns[0]] = df.iloc[:, 0].dt.strftime("%Y%m%d").astype(int)

        df_numpy = df.to_numpy()

        if sector == "T_BILL_3_MO":
            cleaned_data[sector] = removeUnnecessaryData(df_numpy, True)
        else:
            cleaned_data[sector] = removeUnnecessaryData(df_numpy)

    return cleaned_data

def combine_data(data):
    header = ""
    date = np.array([])
    change = np.array([])

    for sector, df in data.items():
        if len(date) == 0:
            date = df[:, 0]
            header = "date"

        if len(change) == 0:
            change = df[:, 1]
        else:
            change = np.column_stack((change, df[:, 1]))

        header += "," + sector

    combined_data = np.column_stack((date, change))
    combined_data[:, 0] = combined_data[:, 0].astype(int)

    return header, combined_data

def process_data(header, data):
    date = data[:, 0]
    t_bill = data[:, 1]
    indices = data[:, 2:]

    diff = indices - t_bill[:, np.newaxis]

    out_data = np.column_stack((t_bill, diff))

    if not os.path.exists(EXPORT_PATH):
        os.mkdir(EXPORT_PATH)

    out_data = pd.DataFrame(out_data, index=date, columns=header.split(",")[1:])
    out_data.index.name = "date"
    out_data.index = out_data.index.astype(int)

    return out_data

def removeUnnecessaryData(data, t_bill=False):
    if (t_bill):
        data[:, ADJ_CLOSE] = data[:, ADJ_CLOSE] / 100
        newData = np.column_stack((data[:, DATE], data[:, ADJ_CLOSE]))
        return newData
    else:
        newData = percentage_change(data[:, OPEN], data[:, ADJ_CLOSE])
        newData = np.column_stack((data[:, DATE], newData))
        return newData


def get_sp_sector():
    if update():
        print("Downloading data...")
        all_data = download()
        monthly_data = to_monthly_data(all_data)
        cleaned_data = clean_data(monthly_data)
        header, combined_data = combine_data(cleaned_data)
        out_data = process_data(header, combined_data)

        out_data.to_csv(os.path.join(EXPORT_PATH, "spsector.csv"))

        f = open(LAST_UPDATE_PATH, "w")
        f.write(str(datetime.datetime.now().date()))
        f.close()
        
    print("Data up to date.")
    
    data = read_data(os.path.join(EXPORT_PATH, "spsector.csv"))
    return data