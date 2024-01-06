import os
import pandas as pd
import zipfile
import requests
from io import BytesIO, StringIO

from util import *

URL_25_PORTFOLIO =  "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/25_Portfolios_5x5_CSV.zip"
URL_10_INDUSTRY = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/10_Industry_Portfolios_CSV.zip"
URL_3_FACTORS = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Developed_3_Factors_CSV.zip"

def download(url):
    response = requests.get(url)
    zip_file = zipfile.ZipFile(BytesIO(response.content))
    zip_file.extractall()

    file_names = zip_file.namelist()

    with open(file_names[0], 'r') as file:
        file_content = file.read()
        
        return file_content

def get_25_portfolio():
    return get("25_portfolio", URL_25_PORTFOLIO)


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
    get("10_industry", URL_10_INDUSTRY)

def get_3_factors():
    return get("3_factors", URL_3_FACTORS)

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

        portfolio['SMB'] = factors['SMB']
        portfolio['HML'] = factors['HML']
        portfolio['Mkt-RF'] = factors['Mkt-RF']
        
        portfolio.dropna(inplace=True)
    
        portfolio.to_csv(os.path.join(EXPORT_PATH, "25_3.csv"))

    print("Data up to date.")

    data = read_data(os.path.join(EXPORT_PATH, "25_3.csv"))
    return data

def get_25_4():
    pass

def get(type, url):
    if update(type):
        print(f"Downloading {type} data...")
        
        data = download(url)
        data_start = data.find("Average Value Weighted Returns -- Monthly") if type != "3_factors" else data.find("Missing data are indicated by -99.99.")
        data_end = data.find("Average Equal Weighted Returns -- Monthly") if type != "3_factors" else data.find("Annual Factors: January-December")
        
        data = data[data_start:data_end]
        df = pd.read_csv(StringIO(data), skiprows=1, engine='python', index_col=0)
        
        df.index.name = 'Date'

        df.to_csv(os.path.join(EXPORT_PATH, f"{type}.csv"))

    print("Data up to date.")

    data = read_data(os.path.join(EXPORT_PATH, f"{type}.csv"))
    return data