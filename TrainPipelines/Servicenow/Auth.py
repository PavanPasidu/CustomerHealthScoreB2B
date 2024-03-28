import requests
import os
from ..Constant import Constant as cons
from fastapi import FastAPI, HTTPException, BackgroundTasks
import json



class Auth:
    def __init__(self,url,const):
        self.url                =   url
        self.username           =   const.USERNAME
        self.password           =   const.PASSWORD
        self.grant_type         =   const.GRANT_TYPE
        self.client_id          =   const.CLIENT_ID
        self.client_secret      =   const.CLIENT_SECRET
        


    def saveAccessToken(self,creds,credential_path):    
        with open(credential_path) as f:
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError as e:
                pass
        empty  = (os.stat(credential_path).st_size == 0)
        if empty:
            data = creds
        else:
            data.update({'ACCESS_TOKEN':creds['ACCESS_TOKEN'],'REFRESH_TOKEN':creds['REFRESH_TOKEN']})
        with open(credential_path, 'w') as f:
            json.dump(data, f)


    def getAccessToken(self,const):
        FILE_PATH   = 'E:/Research/CHS_Repo/CustomerHealthScoreB2B/Tokens/accessTokens.json'

        # Set proper headers
        headers     = {'Content-Type': 'application/x-www-form-urlencoded',
                    'Connection':'keep-alive',}

        # Set the urlencoded body
        username        = const.USERNAME
        password        = const.PASSWORD
        grant_type      = const.GRANT_TYPE
        client_id       = const.CLIENT_ID
        client_secret   = const.CLIENT_SECRET

        data = {'username': username, 'password': password, 'grant_type': grant_type,
                'client_id': client_id, 'client_secret': client_secret}

        # Do the HTTP request
        try:
            response = requests.post(self.url, headers=headers, data=data)
        except requests.exceptions.HTTPError as e:
            print("HTTP error occurred:", e)
        except requests.exceptions.ConnectionError as e:
            print("Connection Error occurred:", e)
        except requests.exceptions.InvalidURL as e:
            print("Invalid URL:", e)

        # Check for HTTP codes other than 200
        if response.status_code != 200:
            print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.json())
            exit()

        # Decode the JSON response into a dictionary and use the data
        data         = response.json()
        accessToken  =   data.get('access_token')

        # Save the access token, refresh token
        try:
            if response.status_code == 200:
                # Extract the access token from the response
                access_token    = data.get("access_token")
                refresh_token   = data.get("refresh_token")
                token_type      = data.get("token_type")
                expires_in      = data.get("expires_in")

                if access_token and refresh_token:
                    self.saveAccessToken(
                        {"ACCESS_TOKEN":access_token, "REFRESH_TOKEN":refresh_token, "TOKEN_TYPE":token_type, "EXPIRES_IN":expires_in}, 
                        FILE_PATH)
                else:
                    raise HTTPException(status_code=500, detail="Failed to obtain access token & refersh token")
            else:
                raise HTTPException(status_code=response.status_code, detail=response.text)
        except HTTPException as e:
            pass
        return accessToken


    '''
    Since access token wil expire in soon, we have to regenerate a new access token everytime it expire. 
    So to prevent that we will use refresh token to generate new access token. It is better than using user credentials
    '''
    def renewAccessToken(self,const,token_url):
        GRANT_TYPE = "refresh_token"
        FILE_PATH  = 'E:/Research/CHS_Repo/CustomerHealthScoreB2B/Tokens/accessTokens.json'

        with open(FILE_PATH) as js:
            CREDENTIALS = json.load(js)
        token_params = {
            "grant_type": GRANT_TYPE,
            "client_id": const.CLIENT_ID,
            "client_secret": const.CLIENT_SECRET,
            "access_token": CREDENTIALS.get("ACCESS_TOKEN"),
            "refresh_token": CREDENTIALS.get("REFRESH_TOKEN")
        }
        token_response = requests.post(token_url, data=token_params)
        print(f"token_response:{token_response}")

        try:
            if token_response.status_code == 200:
                # Extract the access token from the response
                access_token    = token_response.json().get("access_token")
                refresh_token   = token_response.json().get("refresh_token")
                token_type      = token_response.json().get("token_type")
                expires_in      = token_response.json().get("expires_in")

                if access_token and refresh_token:
                    self.saveAccessToken(
                        {"ACCESS_TOKEN":access_token, "REFRESH_TOKEN":refresh_token, "TOKEN_TYPE":token_type, "EXPIRES_IN":expires_in}, 
                        FILE_PATH)
                else:
                    raise HTTPException(status_code=500, detail="Failed to obtain access token & refersh token")
            else:
                raise HTTPException(status_code=token_response.status_code, detail=token_response.text)
        except HTTPException as e:
            pass
        return token_response.status_code
