import os
from arrow import get
import pandas as pd
import zipfile
import requests
from io import BytesIO, StringIO

from .util import *
from .sp_sector import *

URL_25_PORTFOLIO =  "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/25_Portfolios_5x5_CSV.zip"
URL_10_INDUSTRY = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/10_Industry_Portfolios_CSV.zip"
URL_3_FACTORS = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Developed_3_Factors_CSV.zip"
URL_MOM_FACTOR = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Momentum_Factor_CSV.zip"
URL_INTERNATIONAL = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_International_Countries.zip"
URL_WORLD = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_International_Indices.zip"

def download(url):
    response = requests.get(url)

    if response.status_code == 200:
        with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
            zip_file.extractall()

            file_names = zip_file.namelist()

            file_contents = {}

            for file_name in file_names:
                with open(file_name, 'r') as file:
                    file_content = file.read()
                    file_contents[file_name] = file_content

                os.remove(file_name)

            return file_contents

    else:
        print(f"Failed to download. Status code: {response.status_code}")
        return None

def get_25_portfolio():
    return handle_data_standard("25_portfolio", URL_25_PORTFOLIO)

def get_10_industry_riskfree():
    get_10_industry()
    get_3_factors()

    if update("10_industry_riskfree"):
        print("Compiling 10_industry_riskfree data...")

        industry = pd.read_csv(os.path.join(EXPORT_PATH, "10_industry.csv"), index_col=0)
        factors = pd.read_csv(os.path.join(EXPORT_PATH, "3_factors.csv"), index_col=0)

        industry['RF'] = factors['RF']
        industry['Mkt-RF'] = factors['Mkt-RF']

        industry.dropna(inplace=True)
        industry = move_column(industry, 'RF', 0)
    
        industry.to_csv(os.path.join(EXPORT_PATH, "10_industry_riskfree.csv"))

    print("Data up to date.")

    data = read_data(os.path.join(EXPORT_PATH, "10_industry_riskfree.csv"))
    return data

def get_10_industry():
    handle_data_standard("10_industry", URL_10_INDUSTRY)

def get_3_factors():
    return handle_data_standard("3_factors", URL_3_FACTORS)

def get_25_1():
    get_25_portfolio()
    get_3_factors()

    if update("25_1"):
        print("Compiling 25_1 data...")

        factors = pd.read_csv(os.path.join(EXPORT_PATH, "3_factors.csv"), index_col=0)
        portfolio = pd.read_csv(os.path.join(EXPORT_PATH, "25_portfolio.csv"), index_col=0)

        portfolio['Mkt-RF'] = factors['Mkt-RF']
        portfolio['RF'] = factors['RF']

        portfolio.dropna(inplace=True)
        portfolio = move_column(portfolio, 'RF', 0)
    
        portfolio.to_csv(os.path.join(EXPORT_PATH, "25_1.csv"))

    print("Data up to date.")

    data = read_data(os.path.join(EXPORT_PATH, "25_1.csv"))
    return data

def get_25_3():
    get_25_portfolio()
    get_3_factors()

    if update("25_3"):
        print("Compiling 25_3 data...")

        factors = pd.read_csv(os.path.join(EXPORT_PATH, "3_factors.csv"), index_col=0)
        portfolio = pd.read_csv(os.path.join(EXPORT_PATH, "25_portfolio.csv"), index_col=0)

        portfolio['RF'] = factors['RF']
        portfolio['SMB'] = factors['SMB']
        portfolio['HML'] = factors['HML']
        portfolio['Mkt-RF'] = factors['Mkt-RF']
        
        portfolio.dropna(inplace=True)
        portfolio = move_column(portfolio, 'RF', 0)
    
        portfolio.to_csv(os.path.join(EXPORT_PATH, "25_3.csv"))

    print("Data up to date.")

    data = read_data(os.path.join(EXPORT_PATH, "25_3.csv"))
    return data

def get_25_4():
    get_25_portfolio()
    get_3_factors()
    get_mom_factor()

    if update("25_4"):
        print("Compiling 25_4 data...")

        factors = pd.read_csv(os.path.join(EXPORT_PATH, "3_factors.csv"), index_col=0)
        portfolio = pd.read_csv(os.path.join(EXPORT_PATH, "25_portfolio.csv"), index_col=0)
        mom = pd.read_csv(os.path.join(EXPORT_PATH, "mom_factor.csv"), index_col=0)

        portfolio['RF'] = factors['RF']
        portfolio['SMB'] = factors['SMB']
        portfolio['HML'] = factors['HML']
        portfolio['Mkt-RF'] = factors['Mkt-RF']
        portfolio['Mom'] = mom

        portfolio.dropna(inplace=True)
        portfolio = move_column(portfolio, 'RF', 0)

        portfolio.to_csv(os.path.join(EXPORT_PATH, "25_4.csv"))

    print("Data up to date.")

    data = read_data(os.path.join(EXPORT_PATH, "25_4.csv"))
    return data

def get_mom_factor():
    return handle_data_standard("mom_factor", URL_MOM_FACTOR)

def handle_data_standard(type, url):
    if update(type):
        print(f"Downloading {type} data...")
        
        data = download(url)
        first_key = next(iter(data))
        data = data[first_key]
        if type == "3_factors":
            data_start = data.find("Missing data are indicated by -99.99.")
        elif type == "mom_factor":
            data_start = data.find("Missing data are indicated by -99.99 or -999.")
        else:
            data_start = data.find("Average Value Weighted Returns -- Monthly")

        if type == "3_factors":
            data_end = data.find("Annual Factors: January-December")
        elif type == "mom_factor":
            data_end = data.find("Annual Factors:")
        else:
            data_end = data.find("Average Equal Weighted Returns -- Monthly")
        
        data = data[data_start:data_end]
        df = pd.read_csv(StringIO(data), skiprows=1, engine='python', index_col=0)
        
        df.index.name = 'Date'

        df = df.apply(lambda x: x/100.0)

        df.to_csv(os.path.join(EXPORT_PATH, f"{type}.csv"))

    print("Data up to date.")

    data = read_data(os.path.join(EXPORT_PATH, f"{type}.csv"))
    return data

def get_international():
    counties = [
        "Canada",
        "Japan",
        "France",
        "Germany",
        "Italy",
        "Swtzrlnd",
        "UK"
    ]

    if update("international"):
        print("Downloading international data...")

        all_data = download(URL_INTERNATIONAL)
        all_data = {k: v for k, v in all_data.items() if k.split(".")[0].replace(" ", "") in counties}
        all_df = pd.DataFrame()

        for k, v in all_data.items():
            name = k.split(".")[0].replace(" ", "")

            data_start = v.find("-- BE/ME --   --- E/P ---   --- CE/P --   ------  Yld  -----")
            data_end = v.find("Value-Weight Local  Returns      All 4 Data Items Not Reqd")

            data = v[data_start:data_end]
            df = pd.read_csv(StringIO(data), skiprows=1, engine='python', index_col=0, sep='\s+')
            
            df = df.iloc[:, :1]
            df.index.name = 'Date'
            
            df = df.apply(lambda x: x/100.0)

            if all_df.empty:
                all_df.index = df.index
            all_df[name] = df

        all_df.to_csv(os.path.join(EXPORT_PATH, "international.csv"))

    print("Data up to date.")

    data = pd.read_csv(os.path.join(EXPORT_PATH, "international.csv"), index_col=0)
    return data

def get_world():
    if update("world"):
        data = download(URL_WORLD)['Ind_all.Dat']
        df = pd.DataFrame()

        data_start = data.find("-- BE/ME --   --- E/P ---   --- CE/P --   ------  Yld  -----")
        data_end = data.find("Value-Weight Local  Returns      All 4 Data Items Not Reqd")

        data = data[data_start:data_end]
        df = pd.read_csv(StringIO(data), skiprows=1, engine='python', index_col=0, sep='\s+')

        df = df.iloc[:, :1]
        df.index.name = 'Date'
        df.columns = ['World']

        df = df.apply(lambda x: x/100.0)

        df.to_csv(os.path.join(EXPORT_PATH, "world.csv"))

    print("Data up to date.")

    df = pd.read_csv(os.path.join(EXPORT_PATH, "world.csv"), index_col=0)

    return df

def get_full_international():
    if update("full_international"):
        print("Compiling full_international data...")

        t_bill = get_t_bill_3_mo()
        t_bill.index = pd.to_datetime(t_bill.index)
        t_bill.index = t_bill.index.map(lambda x: get(x).format("YYYYMM"))
        t_bill.index = t_bill.index.map(lambda x: int(x))

        usa = get_usa_3_mo()
        usa.index = pd.to_datetime(usa.index)
        usa.index = usa.index.map(lambda x: get(x).format("YYYYMM"))
        usa.index = usa.index.map(lambda x: int(x))

        world = get_world()
        international = get_international()

        df = pd.merge(international, usa, how='right', on='Date')
        df.columns = list(df.columns[:-1]) + ['USA']
        df = pd.merge(df, world, how='right', on='Date')
        df = pd.merge(t_bill, df, how='right', on='Date')

        df.dropna(inplace=True)
        df.to_csv(os.path.join(EXPORT_PATH, "full_international.csv"))

    print("Data up to date.")

    df = read_data(os.path.join(EXPORT_PATH, "full_international.csv"))
    return df