import requests
import pandas as pd
from bs4 import BeautifulSoup 
import numpy as np
from argparse import ArgumentParser
import src.walorder as wa

argparser = ArgumentParser()
argparser.add_argument('-evt', '--EVENT', type=str, default='100-metres', help='referenced event')
argparser.add_argument('-evr', '--ENVRMNT', type=str, default='outdoor', help='referenced environment')
argparser.add_argument('-gdr', '--GENDER', type=str, default='men', help='referenced gender')
argparser.add_argument('-age', '--AGE', type=str, default='senior', help='referenced age')
argparser.add_argument('-num', '--NUMBER', type=int, default=100, help='num of competitors')
argparser.add_argument('-odir', '--ODIR', type=str, default='./', help='output directoty')
args = argparser.parse_args()
#####   Parameter Settings   ##################################################################################

#['100-metres', '400-metres', 'long-jump', 'shot-put', 'decathlon' ,'50-kilometres-race-walk'] etc.
EVENT=args.EVENT

#['outdoor', 'indoor']
ENVRMNT=args.ENVRMNT

#['men','women']
GENDER=args.GENDER

#['Senior', 'u20' 'u18']
AGE=args.AGE

#Number of competitors in your list
MAX_=args.NUMBER

OUTPUT_DIR = args.ODIR
###############################################################################################################

#Genre=['sprints','middle-long','road-running','jumps','throws','combined-events','race-walks','relays'] etc.
GENRE='something'

MAX_page=MAX_/100+1


def main():
    page=1

    while(page<MAX_page):
        #Download
        athletes_profile_html, input_void =wa.load(EVENT, ENVRMNT, GENDER, AGE, GENRE, page)

        #If data is void, this program will be terminated.
        if input_void:
            break

        #Define DataFrame and columns of data
        if page==1:
            df = wa.make_DataFrame(athletes_profile_html, EVENT)


        #Derive DataFrame from html      
        if EVENT=='decathlon' or EVENT=='heptathlon':
            df = wa.html_to_df_combine(athletes_profile_html, df)
        else:
            df = wa.html_to_df(athletes_profile_html, df)
        page +=1
        
    #Split breakdown to each event columns    
    if EVENT=='decathlon' or EVENT=='heptathlon':       
        df = wa.split_combine_breakdown(df, EVENT)
        
        
    df.to_csv(OUTPUT_DIR+'{}-{}_{}_{}.csv'.format(GENDER,EVENT,ENVRMNT,AGE), index=False)
    print(df)

if __name__ == "__main__":
    main()
