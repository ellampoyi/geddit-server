from django.shortcuts import render
#from server.models import User, Errand
from django.views.decorators.csrf import csrf_exempt
from .consumers import authenticate, new_errand, get_listed_errands, create_account
from .consumers import get_profile_from_database
#from .apps import send_topic_push
from django.http import JsonResponse
from firebase_admin import credentials, messaging

# Create your views here.

from django.http import HttpResponse
import json

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# def active_errands(request):
#     return HttpResponse(Errand.objects.filter(status="active"))
#

@csrf_exempt
def login(request):
    print(request.body)
    if request.method == "POST":
        credentials = json.loads(request.body)
        print(credentials)
        if authenticate(credentials['phone'], credentials['hash']):
            return HttpResponse(status=202)
        else:
            send_topic_push('imposter', 'escape')
            return HttpResponse(status=401)
    return HttpResponse(status=401)

@csrf_exempt
def register(request):
    print(request.body)
    if request.method == "POST":
        credentials = json.loads(request.body)
        print(credentials, "Asd")
        if create_account(credentials['phone'], credentials['hash']):
            return HttpResponse(status=202)
        else:
            send_topic_push('imposter', 'escape')
            return HttpResponse(status=401)
    return HttpResponse(status=401)


@csrf_exempt
def get_profile(request):
    print(request.body)
    if request.method == "POST":
        credentials = json.loads(request.body)
        print(credentials)
        if authenticate(credentials['phone'], credentials['hash']):
            profile = get_profile_from_database(credentials['phone'])
            if profile is not None:
                return JsonResponse(profile, status=200, safe=False)
            else:
                return HttpResponse(status=401)
    return HttpResponse(status=401)

@csrf_exempt
def request_errand(request):
    print(request.body)
    if request.method == "POST":
        errand = json.loads(request.body)
        new_errand(errand['from'], errand['to'], errand['desc'], errand['phone'], errand['price'])
        send_topic_push("New Errand", errand['phone'])
        return HttpResponse(status=200)

@csrf_exempt
def listed_errands(request):
    print(request.body)
    if request.method == "GET":
        listed = get_listed_errands()
        print(listed)
        if listed is not None:
            return JsonResponse(listed, status=200, safe=False)
        else:
            return HttpResponse(status=401)
    return HttpResponse(status=401)



def send_topic_push(title, body):
    print("alert")
    topic = 'all'
    message = messaging.Message(notification=messaging.Notification(title=title, body=body), topic=topic)
    messaging.send(message)
