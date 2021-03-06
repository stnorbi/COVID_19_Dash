# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import datetime as datetime
from bs4 import BeautifulSoup as bs
import requests
import sys


now = datetime.datetime.today()
ido = str(now.hour)+':'+str(now.minute)
now = str(now.month)+'/'+str(now.day)+'/'+str(now.year)[2:]


DATA_URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/"
FILE_C = "time_series_covid19_confirmed_global.csv"
FILE_D = "time_series_covid19_deaths_global.csv"
FILE_R = "time_series_covid19_recovered_global.csv"
country_table = {'United Kingdom': 'UK', 'United Arab Emirates': 'UAE', 'USA': 'US', 'Cote d\'Ivoire': 'Ivory Coast',
                 'Congo (Brazzaville)': 'Congo', 'Saint Vincent and the Grenadines': 'St. Vincent Grenadines',
                 'Korea, South': 'S. Korea', 'Taiwan*': 'Taiwan'}

def load_data(the_file, country):
    data = pd.read_csv(the_file)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data.rename(columns={'country/region':'country', 'province/state':'state'}, inplace=True)
    data.fillna(0, inplace=True)
    data = data[data['country'] == country]
    data = data[data.state == 0]
    data = data.groupby(['country']).sum()
    data = data.iloc[:,4:].T
    data = data[(data.T != 0).any()]
    data.rename(columns={data.columns[0]: 'Eset'}, inplace=True)
    return data

def str2int(s):
    if s == ' ':
        return 0
    s = s.replace(',','')
    return int(s) 

def main(the_country):

    df_d = load_data(DATA_URL + FILE_D, the_country) # Halottak
    df_r = load_data(DATA_URL + FILE_R, the_country) # Gyógyultak
    df_c = load_data(DATA_URL + FILE_C, the_country) # Esetek
    df = pd.DataFrame()
    df['Eset'] = df_c['Eset']
    df['Gyógyult'] = df_r['Eset']
    df['Halott'] = df_d['Eset']
    dfT = df.T
    
    if the_country == 'Hungary':
        url='https://koronavirus.gov.hu/'
        page = requests.get(url)
        soup = bs(page.content, 'html.parser')
        c = soup.find_all(class_ = 'number')
        eset = int(c[0].text.replace(" ",""))
        gyogyult = int(c[1].text)
        
        page = requests.get(url+'/elhunytak')
        soup = bs(page.content, 'html.parser')
        c = soup.find(class_ = 'views-row-last')
        c = c.find(class_ = 'views-field-field-elhunytak-sorszam')
        halott = int(c.text)
        dfT[now] = [eset, gyogyult, halott]
    else:
        if the_country in country_table:
            the_country = country_table[the_country]
        url = 'https://www.worldometers.info/coronavirus/#countries'
        page = requests.get(url)
        soup = bs(page.content, 'html.parser')
        tbl = soup.find(id='main_table_countries_today')
        tbl = tbl.findAll('tr')
        eset = -1
        for tr in tbl:
            if the_country in tr.text:
                tds = tr.findAll('td')
                eset = str2int(tds[1].text)
                halott = str2int(tds[3].text)
                gyogyult = str2int(tds[5].text)
                break
        if eset > -1:
            dfT[now] = [eset, gyogyult, halott]
        else:
            print(f'{the_country} is not on [page]({url}).')


    dfT[now] = [eset, gyogyult, halott]
    df = dfT.T

    df.fillna(0, inplace= True)
    df['Aktív'] = df['Eset']-df['Gyógyult'] - df['Halott']
    df = df.astype(int)
    
    df = df.reset_index()
    df.rename(columns = {'index': 'Dátum'}, inplace=True)
    df['Dátum'] = pd.to_datetime(df['Dátum'])
    df.set_index(['Dátum'], drop=True, inplace=True)

    df['Aktív'] = df['Eset']-(df['Gyógyult']+df['Halott'])
    df['Eset+'] = df['Eset'].shift(1)
    df['Halott+'] = df['Halott'].shift(1)
    df.fillna(0, inplace=True)
    df['EsetD'] = abs(df['Eset'] - df['Eset+'])
    df['HalottD'] = abs(df['Halott'] - df['Halott+'])
    df = df.astype(int)
    return df

