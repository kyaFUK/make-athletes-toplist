import requests
import pandas as pd
from bs4 import BeautifulSoup 
import numpy as np

def load(EVENT='100-metres', ENVRMNT='outdoor', GENDER='men', AGE='senior',GENRE='something', page=1):
    html=requests.get('https://www.worldathletics.org/records/all-time-toplists/{}/{}/{}/{}/{}?page={}'.format(GENRE,EVENT,ENVRMNT,GENDER,AGE,page))
    soup = BeautifulSoup(html.content, "html.parser")
    athletes_profile_html=soup.find_all('tr')
    if athletes_profile_html==[]:
        if page==1:
            print("Request Error")
            return athletes_profile_html, True
    else:
        return athletes_profile_html, False

def make_DataFrame(athletes_profile_html, EVENT):
    columns=[]
    for column in athletes_profile_html[0].find_all('th'):
        column=column.text.replace('\n', '').replace(' ', '')
        if len(list(column))>0:
            columns.append(column)
    if EVENT=='decathlon' or EVENT=='heptathlon':
        columns.append('Breakdown')
    return pd.DataFrame(index=[], columns=columns)


def html_to_df_combine(athletes_profile_html, df):
    columns = df.columns
    for athlete , num in zip(athletes_profile_html, range(len(athletes_profile_html))):
        if num%2==1:
            records=athlete.find_all('td')
            series=[]
            for record in records:
                #column=record.get('data-th')
                if record.get('data-th')!=' ':
                    series.append(record.text.replace('\n', '').replace(' ', ''))
                    
        #Deal with 'Breakdown'
        elif num%2==0 and num!=0:
            if(len(series)>0):
                bd=athlete.find_all('td')[1].text
                series.append(bd.replace('(', '').replace(')', ''))
                #print(columns)
                tmp=pd.Series(series, index=columns)
                df = df.append(tmp, ignore_index=True)
    return df

def html_to_df(athletes_profile_html, df):
    columns = df.columns
    for athlete in athletes_profile_html:
        records=athlete.find_all('td')
        series=[]
        for record in records:
            #column=record.get('data-th')
            if record.get('data-th')!=' ':
                series.append(record.text.replace('\n', '').replace(' ', ''))
        if(len(series)>0):
            tmp=pd.Series(series, index=columns)
            df = df.append(tmp, ignore_index=True)
    return df

def split_combine_breakdown(df, EVENT):
    split=df['Breakdown'].str.split(' ', expand=True)

    if EVENT=='decathlon':
        split=split.loc[:,np.arange(1,len(split.columns)-2,2)]
        comb_EVENTS=['100-metres','long-jump', 'shot-put', 'high-jump' ,'400-metres','110-metres-hurdles', 'discus-throw','pole-vault', 'javelin-throw','1500-metres']
        comb_wind = ['100-metres', 'long-jump', '110-metres-hurdles']
    elif EVENT == 'heptathlon':
        split=split.loc[:,np.arange(1,len(split.columns),2)]
        comb_EVENTS=['100-metres-hurdles','high-jump', 'shot-put', '200-metres' ,'long-jump', 'javelin-throw','800-metres']
        comb_wind = ['100-metres-hurdles', '200-metres','long-jump']
    
    split.columns=comb_EVENTS
    for event in comb_wind:
        split_wind=split[event].str.split('/', expand=True)
        split[event]=split_wind[0]
        split[event+'_wind']=split_wind[1]

    df=pd.concat([df,split], axis=1)
    return df