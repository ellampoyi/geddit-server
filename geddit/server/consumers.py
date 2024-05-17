import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db import connection
from django.db import IntegrityError
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from geddit.server.models import AcceptedErrand
from geddit.server.models import ListedErrand
from geddit.server.models import CustomUser as User


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

        if command == 'authenticate':
            password_hash = text_data_json['hash']
            mail = text_data_json['mail']
            # have to get value from sq
            print(authenticate(mail, password_hash))
            await self.send(text_data=json.dumps({
                'command': 'authenticate',
                'status': 1 if authenticate(mail, password_hash) else 0
            }))
            #sendProfile(phone)

        elif command == 'create_new_errand':
            mail = text_data_json['clientMail']
            from_user = text_data_json['from_user']
            to_user = text_data_json['to_user']
            description = text_data_json['description']
            price = text_data_json['price']

            new_errand(from_user, to_user, description, mail, price)

            await self.channel_layer.group_send("campus", {'type': 'broadcast_message',
                                                           'message': json.dumps(display_errands()), })

        elif command == 'register_new_user':
            mail = text_data_json['mail']
            password_hash = text_data_json['hash']
            await self.send(text_data=json.dumps({
                'command': 'register_new_user',
                'status': 1 if create_account(mail, password_hash) else 0
            }))

        #elif command == 'user'

        # Process the message as needed

        # await self.send(text_ddjang ata=json.dumps({
        #    'message': message
        # }))

    async def broadcast_message(self, event):
        # Send the message to the client
        await self.send(text_data=json.dumps({'command': 'availableerrands', 'availableerrands': event['message']}))


def create_account(mail, password):
    try:
        validate_password(password)
        user = User.objects.create_user(mail, mail, password)

    except IntegrityError:
        status = {"status": False,
                  "reason": "user already exists"}
        status_json = json.dumps(status)
        return status_json

    except ValidationError as e:
        status = {"status": False,
                  "reason": list(e.messages)}
        status_json = json.dumps(status)
        return status_json

    else:
        status = {"status": True,
                  "reason": None}
        status_json = json.dumps(status)
        return status_json


# to create an errand when a user posts and errand
def new_errand(from_loc, to_loc, description, mail, price):
    user = User.objects.get(mail=mail)
    errand = ListedErrand(from_user=user, description=description, from_location=from_loc, to_location=to_loc,
                          price=price)
    errand.save()
    return errand.pk


# when a user accepts an errand posted by another user
def accept_errand(errand_id, mail):
    errand = ListedErrand.objects.get(errand_id=errand_id)
    to_user = User.objects.get(mail=mail)
    accepted_errand = AcceptedErrand(to_user=to_user, from_user=errand.from_user, description=errand.description,
                                     from_location=errand.from_location, to_location=errand.to_location,
                                     price=errand.price)
    accepted_errand.save()
    errand.delete()
    return accepted_errand.pk


# when a user cancels an errand that they have accepted
def cancel_errand(errand_id):
    cancelled_errand = AcceptedErrand.objects.get(errand_id=errand_id)
    errand = ListedErrand(from_user=cancelled_errand.from_user, description=cancelled_errand.description,
                              from_location=cancelled_errand.from_location,
                              to_location=cancelled_errand.to_location, price=cancelled_errand.price)
    errand.save()
    cancelled_errand.delete()
    return errand.pk


# when a user deletes an errand that they have posted
def delete_errand(errand_id):
    errand = ListedErrand.objects.get(errand_id=errand_id)
    errand.delete()
    return


# when a user completes an errand that they have accepted
def complete_errand(errand_id):
    errand = AcceptedErrand.objects.get(errand_id=errand_id)
    errand.delete()
    return


def get_profile_from_database(mail):
    my_listed_errands, my_accepted_errands, my_todo_errands = my_errands(mail)

    my_posted_errand_list = []
    my_todo_errand_list = []

    for each in my_listed_errands:
        errand = {'to_user': None,
                  'description': each.description,
                  'price': each.price,
                  'mail': None,
                  'from_loc': each.from_location,
                  'to_loc': each.to_location}
        my_posted_errand_list.append(errand)

    for each in my_accepted_errands:
        errand = {'to_user': each.to_user.name,
                  'description': each.description,
                  'price': each.price,
                  'mail': each.to_user.mail,
                  'from_loc': each.from_location,
                  'to_loc': each.to_location}
        my_posted_errand_list.append(errand)

    for each in my_todo_errands:
        errand = {'to_user': each.to_user.name,
                  'description': each.description,
                  'price': each.price,
                  'mail': each.to_user.mail,
                  'from_loc': each.from_location,
                  'to_loc': each.to_location}
        my_todo_errand_list.append(errand)

    profile_errands_dict = {'mail': mail, 'myPostedErrands': my_posted_errand_list, 'myTodoErrands': my_todo_errand_list}

    profile_errands_json = json.dumps(profile_errands_dict)

    return profile_errands_json


def my_errands(mail):
    # find the user object with mail = mail
    user = User.objects.get(mail=mail)

    # errands that the user has posted but hasnt been accepted
    my_listed_errands = ListedErrand.objects.filter(from_user=user)

    # errands that the user has posted and has been accepted
    my_accepted_errands = AcceptedErrand.objects.filter(from_user=user)

    # errands that the user has accepted and has to do
    my_todo_errands = AcceptedErrand.objects.filter(to_user=user)

    return my_listed_errands, my_accepted_errands, my_todo_errands


def get_listed_errands():
    listed_errands = ListedErrand.objects.all()

    listed_errand_list = []

    for each in listed_errands:
        errand = {'from_loc': each.from_location,
                  'to_loc': each.to_location,
                  'description': each.description,
                  'price': each.price}
        listed_errand_list.append(errand)

    listed_errands_dict = {'listedErrands': listed_errand_list}

    listed_errands_json = json.dumps(listed_errands_dict)

    return listed_errands_json
