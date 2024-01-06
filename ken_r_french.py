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


def get_10_industry():
    return get("10_industry", URL_10_INDUSTRY)

def get_3_factors():
    return get("3_factors", URL_3_FACTORS)

def get(type, url):
    if update(type):
        print(f"Downloading {type} data...")
        data = download(url)
        data_start = data.find("Average Value Weighted Returns -- Monthly") if type != "3_factors" else data.find("Missing data are indicated by -99.99.")
        data_end = data.find("Average Equal Weighted Returns -- Monthly") if type != "3_factors" else data.find("Annual Factors: January-December")
        data = data[data_start:data_end]
        df = pd.read_csv(StringIO(data), skiprows=1, engine='python', index_col=0)
        df.to_csv(os.path.join(EXPORT_PATH, f"{type}.csv"))

    print("Data up to date.")

    data = pd.read_csv(os.path.join(EXPORT_PATH, f"{type}.csv"), index_col=0)
    return data