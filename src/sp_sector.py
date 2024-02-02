from io import StringIO
import os

from .util import *
from .yahoo_finance import *

tickers = {
    "T_BILL_3_MO": "^IRX",
    "SP_CONSUM_DIS": "^SP500-25",
    "SP_HEALTH": "^SP500-35",
    "SP_TELE_COMM": "^SP500-50",
    "SP_FINANCE": "^SP500-40",
    "SP_UTIL": "^SP500-55",
    "SP_500": "^GSPC",
    "SP_CONSUM_STAPLE": "^SP500-30",
    "SP_MATERIALS": "^SP500-15",
    "SP_INFO_TECH": "^SP500-45",
    "SP_ENEGY": "^GSPE"
}

def get_sp_sector():
    if update("spsector"):
        print("Downloading spsector data...")
        all_data = download(tickers)
        monthly_data = to_monthly_data(all_data)
        cleaned_data = clean_data(monthly_data)
        out_data = pd.DataFrame(cleaned_data)

        if not os.path.exists(EXPORT_PATH):
            os.mkdir(EXPORT_PATH)

        out_data.to_csv(os.path.join(EXPORT_PATH, "spsector.csv"))
        
    print("Data up to date.")
    
    data = read_data(os.path.join(EXPORT_PATH, "spsector.csv"))
    return data

def get_t_bill_3_mo():
    data = get_sp_sector()
    df = pd.read_csv(StringIO(data), index_col=0, parse_dates=True)
    return df['T_BILL_3_MO']

def get_usa_3_mo():
    data = get_sp_sector()
    df = pd.read_csv(StringIO(data), index_col=0, parse_dates=True)
    return df['SP_500']