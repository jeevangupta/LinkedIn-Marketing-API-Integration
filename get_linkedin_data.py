#!/usr/bin/python3
import requests
import pandas as pd
import sys
import json
from datetime import datetime, timedelta
import datetime
import re
from urllib import parse

#Function for date validation
def date_validation(date_text):
    try:
        while date_text != datetime.datetime.strptime(date_text, '%Y-%m-%d').strftime('%Y-%m-%d'):
            date_text = input('Please Enter the date in YYYY-MM-DD format\t')
        else:
            return datetime.datetime.strptime(date_text,'%Y-%m-%d')
    except:
        raise Exception('linkedin_campaign_processing : year does not match format yyyy-mm-dd')



def get_campaigns_list(access_token,account):
    try:
        url = "https://api.linkedin.com/v2/adCampaignsV2?q=search&search.account.values[0]=urn:li:sponsoredAccount:"+account

        headers = {"Authorization": "Bearer "+access_token}
        #make the http call
        r = requests.get(url = url, headers = headers)
        
        #defining the dataframe
        campaign_data_df = pd.DataFrame(columns=["campaign_name","campaign_id","campaign_account",
                            "daily_budget","unit_cost","campaign_status","campaign_type"])


        if r.status_code != 200:
            print("\n !! function (get_linkedIn_campaigns_list) something went wrong !! ",r)
        else:
            response_dict = json.loads(r.text)
            
            if "elements" in response_dict:
                campaigns = response_dict["elements"]
                print("\n Total number of campain in account : ",len(campaigns))

                #loop over each campaigns in the account
                campaign_list = []
                for campaign in campaigns:
                    campaign_name = None
                    campaign_id = None
                    campaign_acct = None
                    campaign_obj = None
                    daily_budget = None
                    unit_cost = None
                    tmp_dict = {}

                    #for each campign check the status; ignor DRAFT campaign
                    if "status" in campaign and campaign["status"]!="DRAFT":
                        if "name" in campaign:
                            campaign_name = campaign["name"]
                        tmp_dict["campaign_name"] = campaign_name
                        
                        if "id" in campaign:
                            campaign_id = campaign["id"]
                        tmp_dict["campaign_id"] = campaign_id
                        
                        if "account" in campaign:
                            campaign_acct = campaign["account"]
                            campaign_acct = re.findall(r'\d+',campaign_acct)[0]
                        tmp_dict["campaign_account"] = campaign_acct
                        
                        if "dailyBudget" in campaign:
                            daily_budget = campaign["dailyBudget"]["amount"]
                        tmp_dict["daily_budget"] = daily_budget

                        if "unitCost" in campaign:
                            unit_cost = campaign["unitCost"]["amount"]
                        tmp_dict["unit_cost"] = unit_cost

                        campaign_status = campaign["status"]
                        tmp_dict["campaign_status"] = campaign_status

                        campaign_list.append(tmp_dict)
            else:
                print("\n key *elements* missing in JSON data from LinkedIn")
            
            campaign_data_df = pd.DataFrame.from_records(campaign_list)
            
            try:
                campaign_data_df["daily_budget"] = pd.to_numeric(campaign_data_df["daily_budget"])
                campaign_data_df["unit_cost"] = pd.to_numeric(campaign_data_df["unit_cost"])
            except:
                pass

            return campaign_data_df
    except:
        print("\n !! function get_campaigns_list failed !!",sys.exc_info())



def get_campaign_analytics(access_token,campaigns_ids,s_date,e_date):
    try:
        #calling date validation funtion for start_date format check
        startDate = date_validation(s_date)
        dt = startDate+timedelta(1)
        week_number = dt.isocalendar()[1]
        #calling date validation funtion for end_date format check
        endDate = date_validation(e_date)
        #defining the dataframe
        campaign_analytics_data = pd.DataFrame(columns=["campaign_id","start_date","end_date",
                                    "cost_in_usd","impressions","clicks"])

        fields = "costInUsd, impressions, clicks"

        campaign_list = []
        for cmp_id in campaigns_ids:
            #Building api query in form of url 
            dateRange_start = "dateRange.start.day="+str(startDate.day)+"&dateRange.start.month="+str(startDate.month)+"&dateRange.start.year="+str(startDate.year)
            dateRange_end = "dateRange.end.day="+str(endDate.day)+"&dateRange.end.month="+str(endDate.month)+"&dateRange.end.year="+str(endDate.year)
            
            url = f"https://api.linkedin.com/v2/adAnalyticsV2?q=analytics&pivot=CAMPAIGN&{dateRange_start}&{dateRange_end}&timeGranularity=ALL&campaigns[0]=urn:li:sponsoredCampaign:{str(cmp_id)}&fields={fields}"
            
            #defining header for authentication
            headers = {"Authorization": "Bearer "+access_token}
            
            #make the http call
            r = requests.get(url = url, headers = headers)

            if r.status_code != 200:
                print("\n !! function (get_LinkedIn_campaign) something went wrong !! ",r)
            else:
                response_dict = json.loads(r.text)
                if "elements" in response_dict:
                    campaigns = response_dict["elements"]
                    
                    for campaign in campaigns:
                        tmp_dict = {}
                        cmp_costInUsd = float(campaign["costInUsd"])
                        tmp_dict["cost_in_usd"] = round(cmp_costInUsd,2)

                        cmp_impressions = campaign["impressions"]
                        tmp_dict["impressions"] = cmp_impressions

                        cmp_clicks = campaign["clicks"]
                        tmp_dict["clicks"] = cmp_clicks
                        
                        tmp_dict["campaign_id"] = cmp_id
                    
                        tmp_dict["start_date"] = startDate
                        tmp_dict["end_date"] = endDate
                        

                        tmp_dict["week"] = week_number
                        tmp_dict["month"] = startDate.month
                        
                        campaign_list.append(tmp_dict)
                else:
                    print("\n !! key *elements* missing in JSON data from LinkedIn !!")
        
        campaign_analytics_data = pd.DataFrame.from_records(campaign_list) 
        campaign_analytics_data["start_date"] = startDate
        campaign_analytics_data["end_date"] = endDate

        return campaign_analytics_data
    except:
        print("\n !! function get_campaign_analytics failed !! ",sys.exc_info())


