#!/usr/local/bin/python3
# command to run this code $ python3 ./main.py -s 2024-06-25 -e 2024-06-25
import getopt
import sys
import datetime
import json
import os
from dotenv import load_dotenv
load_dotenv()

from get_linkedin_data import *


def readfile(argv):
    global s_date
    global e_date

    try:
        opts, args = getopt.getopt(argv,"s:e:")
    except getopt.GetoptError:
        usage()
    for opt, arg in opts:
        if opt == '-s':
            s_date = arg
        elif opt == '-e':
            e_date = arg
        else:
            print("Invalid Option in command line")


if __name__ == '__main__':
    try:
        timestamp = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d : %H:%M')
        print("DATE : ",timestamp,"\n")
        print("\n Process start")
        readfile(sys.argv[1:])
        

        access_token = os.getenv("ACCESS_TOKEN")
        account_id = os.getenv("ACCOUNT_ID")

        #call the LinkedIn API query function (i.e get_linkedin_campaign_data)
        ln_campaign_df = get_campaigns_list(access_token,account_id)
        print("\n All Campaigns :\n",ln_campaign_df)

        if not ln_campaign_df.empty:
            #get campaign analytics data
            campaign_ids = ln_campaign_df["campaign_id"]
            campaign_analytics = get_campaign_analytics(access_token,campaign_ids,s_date,e_date)
            print("\n campaigns analytics :\n",campaign_analytics)
        else:
            campaign_analytics = pd.DataFrame()

        print("\n campaigns analytics :\n",campaign_analytics)

        print("\n Process End \n")
    except:
        print("\n Process Failed !! ", sys.exc_info())
