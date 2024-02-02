import datetime
import os
import json
import pandas as pd

LAST_UPDATE_PATH = os.path.join("./data/last_update.json")
EXPORT_PATH = os.path.join("./data")

def update(type):
    last_update = json.loads(read_data(LAST_UPDATE_PATH))
    today = datetime.datetime.now().date()
    today_str = str(today)

    if type not in last_update or last_update[type] != today_str:
        last_update[type] = today_str
    
        f = open(LAST_UPDATE_PATH, "w")
        f.write(json.dumps(last_update))
        f.close()
    
        return True
    
    return False

def read_data(filename):
    if not os.path.exists(filename):
        f = open(filename, "w")
        f.close()
        
        return ""
    else:
        f = open(filename, "r")
        data = f.read()
        f.close()
        
        return data
    
def percentage_change(open, close):
    return (close - open) / open

def move_column(df, column_name, position):
    cols = list(df)
    cols.insert(position, cols.pop(cols.index(column_name)))
    return df.loc[:, cols]

def get_end_date(str):
    df = pd.read_csv(os.path.join(EXPORT_PATH, str + ".csv"), index_col=0, parse_dates=True)
    return df.index[-1]