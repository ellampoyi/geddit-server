from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("auth/login", views.login, name="login"),
    path("auth/register", views.register, name="register"),
    path("users/profile", views.get_profile, name="profile"),
    path("errands/request", views.request_errand, name="request_errand"),
    path("errands/listed", views.listed_errands, name="listed_errands"),
    #path("active_errands", views.active_errands, name="active_errands"),
]
