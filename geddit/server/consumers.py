import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db import connection

cursor = connection.cursor()

class YourConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("hello")
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):

        print(text_data)

        text_data_json = json.loads(text_data)
        command = text_data_json['command']
        
        if command == 'auth':
            hash = text_data_json['hash']
            phone = text_data_json['phone']
# have to get value from sq
            print(authenticate(phone, hash))
            if authenticate(phone, hash):
                await self.send(text_data=json.dumps({
                    'command': 'auth',
                    'status': '1'
                    }))
            else:
                await self.send(text_data=json.dumps({
                    'command': 'auth',
                    'status': '2'
                    }))

            #sendProfile(phone)

            

        elif command == 'newerrand':
            phone = text_data_json['clientPhone']
            froms = text_data_json['from']
            to = text_data_json['to']
            desc = text_data_json['desc']
            price = text_data_json['price']
            
            new_errand(froms, to, desc, phone, price)
            


        elif command == 'reg':
            phone = text_data_json['phone']
            hash = text_data_json['hash']
            if create_account(phone, hash):
                await self.send(text_data=json.dumps({
                    'command': 'reg',
                    'status': '1'
                    }))
            else:
                await self.send(text_data=json.dumps({
                    'command': 'reg',
                    'status': '2'
                    }))

        
        #elif command == 'user'

        

        # Process the message as needed

        # await self.send(text_data=json.dumps({
        #    'message': message
        # }))

def create_account(phone, password):
    cursor.execute("SELECT phone FROM USERS WHERE phone = %s;", [str(phone)])
    #print(len(cursor.fetchall()))
    #print(cursor.fetchall())
    if len(cursor.fetchall()) == 0:
        cursor.execute("INSERT INTO USERS (password, phone) VALUES (%s, %s);", (password, str(phone)))
        connection.commit()
        return True
    else:
        return False

def authenticate(phone, hash):
    cursor.execute("SELECT password FROM USERS WHERE phone = %s", [str(phone)])
    if cursor.fetchone()[0] == hash:
        return True
    else:
        return False

def new_errand(from_loc, to_loc, description, phone, price):
    print(phone)
    cursor.execute("INSERT INTO ERRANDS (from_loc, to_loc, status, phone, description, price) VALUES(%s, %s, '1', %s, %s, %s);", (str(from_loc), str(to_loc), str(phone), description, str(price)))
    cursor.execute("SELECT LAST_INSERT_ID();")
    return cursor.fetchone()[0]

def sendProfile(phone):
    profile_errands = my_errands(phone)
    profile_errands_dict = {'command' : 'profile', 'myerrands' : profile_errands}
    profile_errands_json = json.dumps(profile_errands_dict)

    print(profile_errands_json)

def my_errands(phone):
    cursor.execute("SELECT * FROM ERRANDS WHERE phone = %s", (str(phone)))
    return cursor.fetchall()
