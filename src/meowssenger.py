#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
from clientui import Ui_MainWindow
from startpage import Ui_StartWindow
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow
import requests
import time
from datetime import datetime

class StartPage(QMainWindow, Ui_StartWindow):
    def __init__(self, url):
        super().__init__()
        self.setupUi(self)
        self.url = url
        
        self.startButton.pressed.connect(self.enter_messenger)

    def add_text(self, text):
        self.errorText.clear()
        self.errorText.append(text)
        self.errorText.append("\n")
        self.errorText.repaint()        
       
    def enter_messenger(self):
        name = self.EditLogin.text()
        password = self.EditPassword.text()
        
        if not name or not password:
            self.add_text("Заполните все поля!")    
            return
    
        message = {
           'name':  name,
            'password':  password
            }         

        
        try:
            response = requests.post(f'{self.url}login', json = message)
        except:
            self.add_text("Сервер недоступен")
            return
        
        if response.status_code == 200:
            window.close()
            self.message_window = MessengerApp('http://localhost:5000/', name, password)
            #window = MessengerApp('http://c3e34ab06c97.ngrok.io/')
            self.message_window.show()
            
        elif response.status_code == 401:
            self.add_text("Неверный логин/пароль")
        else:
            self.add_text("Ошибка!") 



class MessengerApp(QMainWindow, Ui_MainWindow):
    def __init__(self, url, name, password):
        super().__init__()
        self.setupUi(self)
        
        self.url = url
        self.name = name
        self.password = password
            
        
        self.pushButton.pressed.connect(self.send_message)
        self.logout.pressed.connect(self.to_start)
        
        self.after = time.time() -24*60*60
        
        self.SayHello.setText("Hello, %s! Let's chat! 🐾" % self.name)
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_messages)
        self.timer.start(1000)
        
    def add_text(self, text):
        self.textBrowser.append(text)
        self.textBrowser.append("\n")
        self.textBrowser.repaint()
        
    def format_message(self, message):
        name = message['name']
        text = message['text']
        dt=datetime.fromtimestamp(message['time'])
        dt_beauty = dt.strftime('%Y/%m/%d %H:%m:%s')
        return f'{name} {dt_beauty}\n{text}\n'
        #return "{} {}\n{}".format(name,dt_beauty,text)  
        
    def update_messages(self):
        try:
            #self.response = requests.get( '{}messages'.format(self.url), params={'after': self.after})
            self.response = requests.get( f'{self.url}messages', params={'after': self.after}) 
            #можно одной строкой http://localhost:5000/messages?after=0
            messages = self.response.json()['messages']
            for message in messages:
                self.add_text(self.format_message(message))
                self.after = message['time']         
        except:
            pass
        
    
    def send_message(self):
        text = self.textEdit.toPlainText()
        
        """
        name = self.lineEditLogin.text()
        password = self.lineEditPassword.text()
        flag = True
        if not name:
            flag = False
            is_empty = "name"           
        elif not password:
            flag = False
            is_empty = "password"
        elif not text:
            flag = False
            is_empty = "message"
        if flag == False:
            self.add_text("Заполните поле \"%s\"" % is_empty)    
            return
        """
        
        if not text:
            self.add_text("Enter your message please")    
            return
         #TODO: perenesti v bd
        self.bot_actions={"1" : "OM-NOM-NOM Yumi!", "2" : "Let's play!", "3" : "Z-z-z...","4" : "ОСТОНОВИС ПОДУМОЙ", "/start cat-bot" : "MEOW!\nPlease choose the command:\n1 - Treat with fish\n2 - Throw a ball\n3 - Put to bed\n4 - Call chubby"}
        #TODO:perenesti na server
        if text=="/start cat-bot" or (text in self.bot_actions and self.bot_flag == True):
            self.bot_flag = True
            self.text = self.bot_actions[text]
            """
            message = {
                'name': 'Cat-bot',
                'password': '111',
                'text': self.text
                }   
            """    
            message = {
                'name': 'Cat-bot',
                'text': self.text,
                'type': 'O',
                'receiver': 'Main chat'
                }   
        else:
            self.bot_flag = False
            """
            message = {
                'name':  self.name,
                'password':  self.password,
                'text': text
                }       
            """
            message = {
                'name':  self.name,
                'text': text,
                'type': 'O',
                'receiver': 'Main chat'
                }   
        try:
            #response = requests.post('{}send'.format(self.url), json=message)
            response = requests.post(f'{self.url}send', json = message)
        except:
            self.add_text("Сервер недоступен")
            return
        
        if response.status_code == 200:
            self.textEdit.setText("")
            self.textEdit.repaint()
        elif response.status_code == 401:
            self.add_text("Неверный логин/пароль")
        else:
            self.add_text("Ошибка!") 
            
    def to_start(self):
        window.message_window.close()
        #window2.close()
        window.EditPassword.setText("")
        window.show()



app = QtWidgets.QApplication([])
window = StartPage('http://localhost:5000/')

#window = MessengerApp('http://c3e34ab06c97.ngrok.io/')
#/Users/elyneagapova/eclipse-workspace/Messenger/src/ngrok http 5000
window.show()
app.exec_()
                        
#app = QtWidgets.QApplication([])
#window = MessengerApp('http://localhost:5000/')
#window = MessengerApp('http://c3e34ab06c97.ngrok.io/')
#/Users/elyneagapova/eclipse-workspace/Messenger/src/ngrok http 5000
#window.show()
#app.exec_()
