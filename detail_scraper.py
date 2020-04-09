import pandas as pd
import numpy as np
import datetime as datetime
from bs4 import BeautifulSoup as bs
import requests

def detail_table():
    url='https://koronavirus.gov.hu/'
    page = requests.get(url)
    soup = bs(page.content, 'html.parser')
    c = soup.find_all(class_ = 'number')
    eset = int(c[0].text)
    gyogyult = int(c[1].text)

    hf = pd.read_html('https://koronavirus.gov.hu/elhunytak')
    hf = pd.DataFrame(hf[0])
    hf.drop(['Sorszám'], axis=1, inplace = True)
    return hf

def avg_ages(hf):
    avg_man = round(hf[hf['Nem'] == 'Férfi'].Kor.mean(),2)
    avg_wmn = round(hf[hf['Nem'] == 'Nő'].Kor.mean(),2)
    return avg_man, avg_wmn

def dist_gend(hf):
        hf.drop(['Alapbetegségek'], axis=1, inplace = True)
        gr = hf.groupby(['Nem']).count()
        gr.rename(columns = {'Kor': 'Eset/Nem'}, inplace = True)
        return gr

def dist_age(hf):
    ages = lambda x: int(str(x)[:-1]+'0')
    hf['Kor'] = hf['Kor'].apply(ages)
    hf = hf.groupby(hf['Kor']).count()
    hf.rename(columns = {'Nem': 'Eset/Korcsoport'}, inplace = True)
    return hf

