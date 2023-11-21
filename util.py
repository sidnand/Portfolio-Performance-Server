import datetime
import os

LAST_UPDATE_PATH = os.path.join("./data/last_update.txt")
EXPORT_PATH = os.path.join("./data")

def update():
    last_update = read_data(LAST_UPDATE_PATH)

    if len(last_update) == 0 or str(last_update) != str(datetime.datetime.now().date()):
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