'''
Created on 12 июл. 2020 г.

@author: elyneagapova
'''

from flask import Flask, request, abort
from datetime import datetime
import time
import sqlite3

conn = sqlite3.connect("meowssenger.db", check_same_thread = False )
cursor = conn.cursor()

#making app on server (localhost)

app = Flask(__name__)


messages = [
    {"name" : "Akiko", "time" : time.time(), "text": "123"},
    {"name" : "Akiko", "time" : time.time(), "text": "1234"}
    ]
users = {
    "Akiko" : "12345",
    "Cat-bot" : "111"
    }

def get_password(name):
    cursor.execute("select Password from Users where Username='%s'" % name)
    try:
        return cursor.fetchall()[0][0]
    except IndexError:
        return None
    
def sign_up(name, password):
    cursor.execute("select MAX(Id) from Users ")
    id = cursor.fetchall()[0][0]+1
    user = [(id, name, password)]
    cursor.executemany("INSERT INTO Users VALUES (?,?,?)", user)
    conn.commit()
    
def save_message(name, time, text, type, receiver):
    cursor.execute("select MAX(Id) from Messages ")
    id = cursor.fetchall()[0][0]+1
    message = [(id, name , time, text, type, receiver)]
    cursor.executemany("INSERT INTO Messages VALUES (?,?,?,?,?,?)", message)
    conn.commit()
    return
"""
def filter_for_dicts(elements, key, min_value):
    new_elements = []
    for element in elements:
        if element[key] > min_value:
            new_elements.append(element)
    
    return new_elements
"""
def filter_messages(key, min_value):
    cursor.execute("select * from Messages where %s > %d" % (key, min_value))
    new_messages = []
    for row in cursor:
        new_messages.append({"name": row[1] , "time": row[2], "text": row[3]})
    print(new_messages)    
    return new_messages

#making pages 

@app.route("/")
def index_view():
    return "Hello, user! <br><a href='/status'>Check status</a>"


#making status page
@app.route("/status")
def status_view():
    return {
    'status' : True ,
    'name' : "Python Messenger",
    'time1' : datetime.now().isoformat(),
    #'time2' : datetime.now().strftime('%Y/%m/%d %H:%m:%s'), # обратное - strptime(). табличка с форматами на сайте пайтон
    #'time3' : time.time(), #со времен эпохи unixю удобно сравнивать
    #'time3' : time.asctime() #в читабельном формате
    'users' : len(users),
    'messages': len(messages)
    }

#sending messages
@app.route("/send", methods=['POST'])
def send_view():
    name = request.json.get('name')
    #password = request.json.get('password')
    text = request.json.get('text')
    type = request.json.get('type')
    receiver = request.json.get('receiver')
    if not isinstance(text, str) or not text or len(text) > 1024:
        abort(400)
    save_message(name, time.time(), text, type, receiver)
    """
    messages.append({'name' : name, 'time' : time.time(), 'text': text})
    """
    return { 'ok' : True }
    

@app.route("/login", methods=['POST'])
def login_view():
    name = request.json.get('name')
    password = request.json.get('password')
    
    for token in [name,password]:
        if not isinstance(token, str) or not token or len(token) > 1024:
            abort(400)
    """        
    if name in users:
        if users[name] !=password:
            abort(401)
    else:
        #sign up
        users[name] = password
    """ 
    pwd = get_password(name)
    if not pwd == None:
        if not pwd == password:
            abort(401)
    else:
        sign_up(name, password)
    return { 'ok' : True }
    

#getting messages
@app.route("/messages")
def messages_view():
    try:
        after = float(request.args['after']) #вытащит из get запроса http://localhost:5000/messages?after=*  аргумент after (строка) и преобразует в число
    except:
        abort(400)
    """
    filtered_messages = filter_for_dicts(messages, 'time', after)
    """
    filtered_messages = filter_messages('time', after)
    return { 'messages' : filtered_messages} 
    
    
      
app.run()

