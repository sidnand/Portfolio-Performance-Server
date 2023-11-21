import datetime
import os
import pandas as pd
import numpy as np
import zipfile
import requests
from io import BytesIO

URL_25_PORTFOLIO =  "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/25_Portfolios_5x5_CSV.zip"
URL_10_INDUSTRY = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/10_Industry_Portfolios_CSV.zip"
URL_3_FACTORS = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/Developed_3_Factors_CSV.zip"

def download(url):
    response = requests.get(URL_25_PORTFOLIO)
    zip_file = zipfile.ZipFile(BytesIO(response.content))
    zip_file.extractall()

    file_names = zip_file.namelist()

    with open(file_names[0], 'r') as file:
        file_content = file.read()
        
        return file_content

def get_25_portfolio():
    data = download(URL_25_PORTFOLIO)
    print(data)


def get_10_industry():
    data = download(URL_10_INDUSTRY)
    print(data)

def get_3_factors():
    data = download(URL_3_FACTORS)
    print(data)

# get_25_portfolio()