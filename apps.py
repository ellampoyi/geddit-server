from django.apps import AppConfig
import firebase_admin
from firebase_admin import credentials


def initialize_firebase():
    firebase_cred = credentials.Certificate("geddit-firebase-service.json")
    firebase_application = firebase_admin.initialize_app(firebase_cred)
    return firebase_application


firebase_app = initialize_firebase()


class ServerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "server"

    def ready(self):
        print("hello")