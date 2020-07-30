import requests
import time
from datetime import datetime


def format_message(message):
    name = message['name']
    text = message['text']
    dt=datetime.fromtimestamp(message['time'])
    dt_beauty = dt.strftime('%Y/%m/%d %H:%m:%s')
    return f'{name} {dt_beauty}\n{text}\n'
    
    
after= time.time() -24*60*60
while True:
    response = requests.get('http://localhost:5000/messages', params={'after': after}) #можно одной строкой http://localhost:5000/messages?after=0
    messages = response.json()['messages']
    for message in messages:
        print(format_message(message))
        after=message['time']
    time.sleep(1) # приостановка программы на секунду, чтобы не убить сервер