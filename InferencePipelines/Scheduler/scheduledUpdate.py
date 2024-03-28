'''Here I will call the sentiment API to get sentiment Account wise.
   And accordingly healthscore will be updated. (Sentiment values will come as batches)
'''

from datetime import date,timedelta
from fastapi import FastAPI,BackgroundTasks
from apscheduler.schedulers.background import BackgroundScheduler as scheduler
import requests
import time

sentimentPayload  =  None
start   = end     = date.today() - timedelta(days=1)

params       = {
    'start':start,
    'end':end,
}
api_endpoint = "http://127.0.0.1:8000/get_comments"

def updateHealthscore():
    print("Healthscore updated!!!!")
    pass

def get_json_payload(api_endpoint,params):
    global sentimentPayload
    try:
        response = requests.get(api_endpoint,params=params)
        response.raise_for_status()  
        sentimentPayload = response.json()
        print("Retrieved the payload!!!!!")
        return sentimentPayload
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        return None


sch = scheduler()
sch.add_job(get_json_payload,trigger='cron', args=(api_endpoint,params) ,hour=9,  minute=20)
sch.add_job(updateHealthscore,trigger='cron',hour=11,  minute=20)
sch.start()
try:
    print('Scheduler started, ctrl+c to exit!')
    while 1:
        pass
except KeyboardInterrupt:
    if sch.state:
        sch.shutdown()

sch.add_job(func=get_json_payload,args=(api_endpoint,params))