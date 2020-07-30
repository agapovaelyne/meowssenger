import requests

name = input('Имя: ')
password = input('Пароль: ')

bot_flag = False
bot_actions={"1" : "OM-NOM-NOM Yumi!", "2" : "Let's play!", "3" : "Z-z-z...","4" : "ОСТОНОВИС ПОДУМОЙ", "/start cat-bot" : "MEOW!\nPlease choose the command:\n1 - Дать рыбку\n2 - Кинуть мячик\n3 - Уложить спать\n4 - Назвать толстым"}

while True:
    text = input('Сообщение: ')
    if text=="/start cat-bot" or (text in bot_actions and bot_flag == True):
        bot_flag = True
        text = bot_actions[text]
        message = {
            'name': 'Cat-bot',
            'password': '111',
            'text': text
            }
    else:
        bot_flag = False
        message = {
            'name':  name,
            'password':  password,
            'text': text
            }
    response = requests.post('http://127.0.0.1:5000/send', json=message)