import requests
import os
from ..Constant import Constant as cons
from fastapi import FastAPI, HTTPException, BackgroundTasks
import json
from .Auth import Auth



class GetServicenowData(Auth):
    def __init__(self,url,const):
        super().__init__(url,const)
        self.url                =   url
           

    '''Get payload from servicenow'''
    def getJSONpayload(self,url,const):
        # Set Header
        headers         = {'Content-Type': 'application/x-www-form-urlencoded'}
        FILE_PATH       = './Tokens/accessTokens.json'

        # Get the access token
        with open(FILE_PATH,'w+') as js:
            try:
                CREDENTIALS = json.load(js)
            except json.decoder.JSONDecodeError as je:
                pass
        empty               = (os.stat(FILE_PATH).st_size == 0)
        if empty:
            accessToken     =   super().getAccessToken(const=const)
        else:
            accessToken     =   CREDENTIALS.get('ACCESS_TOKEN')


        # Headers including Authorization with Bearer token
        headers = {
            'Authorization': f'Bearer {accessToken}',
            'Content-Type': 'application/json'
        }

        params = {
            'startDate':'2022-02-01',
            'endDate':'2022-08-01'
        }

        # Make GET request to ServiceNow Scripted REST API (get_ticket_history)
        response = requests.get(url, headers=headers,params=params)

        # Check if request was successful (status code 200)
        if response.status_code == 200:
            # Retrieve JSON payload from response
            json_payload = response.json()
            # print(json_payload)
        else:
            print(f"Failed to retrieve data: {response.status_code} - {response.text}")
        return json_payload
    

