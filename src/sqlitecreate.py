import sqlite3
import time
from datetime import datetime

conn = sqlite3.connect("meowssenger.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE if not exists Users
                  (Id integer PRIMARY KEY, Username text, Password text)
               """)

conn.commit()

cursor.execute("""CREATE TABLE if not exists Messages
                  (Id integer PRIMARY KEY, Name text, Time real, Text text, Type text, Receiver text)
               """)

conn.commit()

"""

Users = [(1, "Cat-bot" , "111"),
         (2, "Akiko" , "12345"),
         (3, "Elyne" , "3313")]


cursor.executemany("INSERT INTO Users VALUES (?,?,?)", Users)
conn.commit()

Messages = [(1, "Akiko" , time.time(), "First message", "O", "Main chat")]

cursor.executemany("INSERT INTO Messages VALUES (?,?,?,?,?,?)",Messages)
conn.commit()


n = cursor.execute("select * from Messages")
for row in n:
    print(str(row))
    
"""  
name = "Akiko"

def get_password(name):
    cursor.execute("select Password from Users where Username='%s'" % name)
    try:
        return cursor.fetchall()[0][0]
    except IndexError:
        return None
key = 'Time'
min_value = 0
cursor.execute("select * from Messages where %s > %d" % (key, 1595787787.4341602))
#print(cursor.fetchall())

n= datetime.now().strftime('%Y-%m-%d %H:%m:%S') #string
print(n)
p= time.strptime(n,'%Y-%m-%d %H:%M:%S')# в timestruct
print(time.mktime(p))

print (time.time())
print (time.time())
for row in cursor:
    print(row)
 

    
