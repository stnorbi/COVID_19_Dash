import pandas as pd
import numpy as np
import datetime as datetime
from bs4 import BeautifulSoup as bs
import requests
import dash
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def detail_table():
    url='https://koronavirus.gov.hu/'
    page = requests.get(url)
    soup = bs(page.content, 'html.parser')
    c = soup.find_all(class_ = 'number')
    eset = int(c[0].text.replace(" ",""))
    gyogyult = int(c[1].text)

    hf=pd.read_html('https://koronavirus.gov.hu/elhunytak?page=0')
    hf=pd.DataFrame(hf[0])
    hf_tmp=hf

    i=1
    while len(hf_tmp)>0:
      try:  
        hf_tmp = pd.read_html('https://koronavirus.gov.hu/elhunytak?page='+str(i))
        if hf_tmp is not None:
            hf_tmp = pd.DataFrame(hf_tmp[0])
            hf=hf.append(hf_tmp,ignore_index=True)
        i+=1
      except:
            break

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
        nem=gr.index.to_list()
        return gr,nem

def dist_age(hf):
    ages = lambda x: int(str(x)[:-1]+'0')
    hf['Kor'] = hf['Kor'].apply(ages)
    hf = hf.groupby(hf['Kor']).count()
    hf.rename(columns = {'Nem': 'Eset/Korcsoport'}, inplace = True)
    return hf


def county_data():
    scope = ['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
            'credential/dash-tutorial-e41737b72ffc.json', scope) # Your json file here

            

    gc = gspread.authorize(credentials)

    wks = gc.open_by_url("https://docs.google.com/spreadsheets/d/1e4VEZL1xvsALoOIq9V2SQuICeQrT5MtWfBm32ad7i8Q/edit?usp=sharing").worksheet('megyei')

    data = wks.get_all_values()
    headers = data.pop(0)

    df = pd.DataFrame(data, columns=headers)

    df=df.set_index('Dátum')

    

    return df
