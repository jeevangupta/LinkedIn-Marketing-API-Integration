#!/usr/bin/python3
# python3 ./linkedin_ads_account.py

# The code gets the Auth User's LinkedIn Campaign Manager Account Details
import requests
import json
import pandas as pd
import sys
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()


def get_linkedin_ads_account(access_token):
    try:
        url =  "https://api.linkedin.com/v2/adAccountsV2?q=search&search.type.values[0]=BUSINESS&search.status.values[0]=ACTIVE" 
        headers = {"Authorization": "Bearer "+access_token}
        
        #make the http call
        response = requests.get(url = url, headers = headers)

        #define a data frame to store the Linkedin account details
        account_df = pd.DataFrame()

        if response.status_code != 200:
            print("\n !! something went wrong !! Response: ",response)
        else:
            result = json.loads(response.text)
            
            if "elements" in result:
                accounts = result["elements"]
                account_list = accounts
        
        account_df = pd.DataFrame.from_records(account_list) 
        return account_df
    except:
        print("\n !! function get_linkedin_ads_account Failed *** ",sys.exc_info())
        raise



if __name__ == '__main__':
    try:
        timestamp = datetime.strftime(datetime.now(),'%Y-%m-%d : %H:%M')
        print("DATE : ",timestamp,"\n")
        print("LinkedIn Ads Account data extraction process Starts")
 
        access_token = os.getenv("ACCESS_TOKEN")
 
        #call authentication function
        accounts_details_df = get_linkedin_ads_account(access_token)

        #print("\n Account Details :\n",accounts_details_df)
        print("\n Account Details :\n",accounts_details_df[["id","name","status","currency"]])
 
        print("\n Linkedin Ads Account data extraction process Finished")
    except:
        print("\n !! Linkedin Ads Account data extraction process Failed !! ", sys.exc_info())