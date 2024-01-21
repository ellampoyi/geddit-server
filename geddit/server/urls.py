from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    #path("active_errands", views.active_errands, name="active_errands"),
]
