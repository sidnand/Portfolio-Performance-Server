import datetime
import os
import json

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