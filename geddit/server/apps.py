from django.apps import AppConfig
from django.db import models, connection
# from django.db.models import Count, F, Value
# from django.db.models.functions import Length, Upper
# from django.db.models.lookups import GreaterThan
# from django.db.models.expressions import RawSQL
import firebase_admin
from firebase_admin import credentials, messaging

firebase_cred = credentials.Certificate("geddit-firebase-service.json")
firebase_app = firebase_admin.initialize_app(firebase_cred)

class ServerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "server"

    def ready(self):
        print("hello")

        cursor = connection.cursor()


#    cursor.execute("CREATE TABLE IF NOT EXISTS USERS (password VARCHAR(255), phone VARCHAR(10) PRIMARY KEY);")
# cursor.execute("CREATE TABLE IF NOT EXISTS ERRANDS (id INT AUTO_INCREMENT PRIMARY KEY, order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, from_loc INT, to_loc INT, status INT, phone VARCHAR(10), FOREIGN KEY (phone) REFERENCES USERS(phone), description VARCHAR(255), price INT);")
#    cursor.execute("CREATE TABLE IF NOT EXISTS ERRANDS (id INT AUTO_INCREMENT PRIMARY KEY, order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, from_loc INT, to_loc INT, status INT, phone VARCHAR(10), description VARCHAR(255), price INT);")

        cursor.execute("CREATE TABLE IF NOT EXISTS USERS (password VARCHAR(255), phone VARCHAR(10) PRIMARY KEY);")
# cursor.execute("CREATE TABLE IF NOT EXISTS ERRANDS (id INT AUTO_INCREMENT PRIMARY KEY, order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, from_loc INT, to_loc INT, status INT, phone VARCHAR(10), FOREIGN KEY (phone) REFERENCES USERS(phone), description VARCHAR(255), price INT);")
        cursor.execute("CREATE TABLE IF NOT EXISTS ERRANDS (id BIGSERIAL PRIMARY KEY, order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, from_loc INT, to_loc INT, status INT, phone VARCHAR(10), dphone VARCHAR(10), description VARCHAR(255), price INT);")
