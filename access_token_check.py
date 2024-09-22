#!/usr/bin/python3

import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()


def test_token(access_token):
    
    url = "https://api.linkedin.com/v2/me"

    headers = {"Authorization": "Bearer "+access_token}
    #make the http call
    r = requests.get(url = url, headers = headers)

    if r.status_code != 200:
        print("something went wrong :",r)
    else:
        response_dict = json.loads(r.text)
        print("Account Description :\n",response_dict)


if __name__ == '__main__':
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    print(f"\n Client ID is {client_id}")

    test_token(access_token)
   

    