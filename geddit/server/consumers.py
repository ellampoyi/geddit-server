import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db import connection

cursor = connection.cursor()

class YourConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("hello")
        await self.channel_layer.group_add("campus", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("campus", self.channel_name)

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
            
            await self.channel_layer.group_send("campus", {'type': 'broadcast_message', 'message': json.dumps(display_errands()), })


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

        # await self.send(text_ddjang ata=json.dumps({
        #    'message': message
        # }))
    async def broadcast_message(self, event):
        # Send the message to the client
        await self.send(text_data=json.dumps({'command': 'availableerrands', 'availableerrands': event['message']}))


def create_account(phone, password):
    cursor.execute("SELECT phone FROM USERS WHERE phone = %s;", [str(phone)])
    print("Asdas")
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
    user = cursor.fetchone()

    if user is None:
        return False
    if user[0] == hash:
        return True
    else:
        return False

def new_errand(from_loc, to_loc, description, phone, price):
    print(phone)
    cursor.execute("INSERT INTO ERRANDS (from_loc, to_loc, status, phone, description, price) VALUES(%s, %s, '1', %s, %s, %s);", (str(from_loc), str(to_loc), str(phone), description, str(price)))
    cursor.execute("SELECT LAST_INSERT_ID();")
    return cursor.fetchone()[0]

def get_profile_from_database(phone):
    print(phone)


    profile_my_errands = my_errands(phone)

    print(profile_my_errands)

    my_errand_list = []
    
    for each in profile_my_errands:
        errand = {}
        errand['from'] = each[0]
        errand['to'] = each[1]
        errand['desc'] = each[2]
        errand['price'] = each[3]
        errand['phone'] = each[4]
        errand['dphone'] = each[5]
        my_errand_list.append(errand)
    
    print(my_errand_list)

    

    profile_errands_dict = {'phone': phone, 'myErrands': my_errand_list}

    print(profile_errands_dict)

    profile_errands_json = json.dumps(profile_errands_dict)

    print(profile_errands_json)

    return profile_errands_json

def my_errands(phone):
    cursor.execute("SELECT from_loc, to_loc, description, price, phone, dphone FROM ERRANDS WHERE phone = %s", [str(phone)])
    return cursor.fetchall()

def get_listed_errands():
    cursor.execute("SELECT from_loc, to_loc, description, price FROM ERRANDS WHERE status=1 AND order_time > (CURRENT_TIMESTAMP - INTERVAL '3 HOUR')")
    
    profile_listed_errands = cursor.fetchall()

    listed_errand_list = []

    for each in profile_listed_errands:
        errand = {}
        errand['from'] = each[0]
        errand['to'] = each[1]
        errand['desc'] = each[2]
        errand['price'] = each[3]
        listed_errand_list.append(errand)

    print(listed_errand_list)

    listed_errands_dict = {'listedErrands': listed_errand_list}

    print(listed_errands_dict)

    listed_errands_json = json.dumps(listed_errands_dict)

    print(listed_errands_json)

    return listed_errands_json

