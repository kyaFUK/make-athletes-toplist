import requests
import pandas as pd
from bs4 import BeautifulSoup 

#####   Parameter Settings ##################################################################################

#['100-metres', '400-metres', 'long-jump', 'shot-put', 'decathlon' ,'50-kilometres-race-walk'] etc.
EVENTS='100-metres'

#['Outdoor', 'Indoor']
ENVRMNT='outdoor'

#['men','women']
GENDER='men'

#['Senior', 'U20' 'U18']
AGE='senior'

#Number of competitors in your list
MAX_=100
##############################################################################################################

#Genre=['sprints','middle-long','road-running','jumps','throws','combined-events','race-walks','relays'] etc.
GENRE='something'

MAX_page=MAX_/100+1
page=1


while(page<MAX_page): 
    html=requests.get('https://www.worldathletics.org/records/all-time-toplists/{}/{}/{}/{}/{}?page={}'.format(GENRE,EVENTS,ENVRMNT,GENDER,AGE,page))
    soup = BeautifulSoup(html.content, "html.parser")
    athletes=soup.find_all('tr')
    if athletes==[]:
        if page==1:
            print("Request Error")
        break

    if page==1:
        #columnの定義
        columns=[]
        for column in athletes[0].find_all('th'):
            column=column.text.replace('\n', '').replace(' ', '')
            if len(list(column))>0:
                columns.append(column)
        if EVENTS=='decathlon' or EVENTS=='heptathlon':
            columns.append('Breakdown')
        df = pd.DataFrame(index=[], columns=columns)



                
    if EVENTS=='decathlon' or EVENTS=='heptathlon':
        for athlete , num in zip(athletes, range(len(athletes))):
            if num%2==1:
                records=athlete.find_all('td')
                series=[]
                for record in records:
                    #column=record.get('data-th')
                    if record.get('data-th')!=' ':
                        series.append(record.text.replace('\n', '').replace(' ', ''))

            elif num%2==0 and num!=0:
                if(len(series)>0):
                    bd=athlete.find_all('td')[1].text
                    series.append(bd.replace('(', '').replace(')', ''))
                    tmp=pd.Series(series, index=columns)
                    df = df.append(tmp, ignore_index=True)
                    
    else:
        for athlete in athletes:
            records=athlete.find_all('td')
            series=[]
            for record in records:
                #column=record.get('data-th')
                if record.get('data-th')!=' ':
                    series.append(record.text.replace('\n', '').replace(' ', ''))
            if(len(series)>0):
                tmp=pd.Series(series, index=columns)
                df = df.append(tmp, ignore_index=True)
                
    page +=1

df.to_csv('{}-{}_{}_{}.csv'.format(GENDER,EVENTS,ENVRMNT,AGE), index=False)
print(df)