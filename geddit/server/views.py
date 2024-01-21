from django.shortcuts import render
#from server.models import User, Errand

# Create your views here.

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# def active_errands(request):
#     return HttpResponse(Errand.objects.filter(status="active"))
# 
