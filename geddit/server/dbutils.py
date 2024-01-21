import mariadb
from django.db import models, connection
# from django.db.models import Count, F, Value
# from django.db.models.functions import Length, Upper
# from django.db.models.lookups import GreaterThan
# from django.db.models.expressions import RawSQL
import sys

cursor = connection.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS DATABASEPOYI;")

connection.select_db('DATABASEPOYI')

cursor.execute("CREATE TABLE IF NOT EXISTS USERS (password VARCHAR(255), phone VARCHAR(10) PRIMARY KEY);")
# cursor.execute("CREATE TABLE IF NOT EXISTS ERRANDS (id INT AUTO_INCREMENT PRIMARY KEY, order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, from_loc INT, to_loc INT, status INT, phone VARCHAR(10), FOREIGN KEY (phone) REFERENCES USERS(phone), description VARCHAR(255), price INT);")
cursor.execute("CREATE TABLE IF NOT EXISTS ERRANDS (id INT AUTO_INCREMENT PRIMARY KEY, order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, from_loc INT, to_loc INT, status INT, phone VARCHAR(10), description VARCHAR(255), price INT);")

# status 0 = unallocated errand 1 = allocated errand

def create_account(phone, password):
    cursor.execute("SELECT phone FROM USERS WHERE phone = %s;", str(phone))
    print(len(cursor.fetchall()))
    if len(cursor.fetchall()) == 0:
        cursor.execute("INSERT INTO USERS (password, phone) VALUES (%s, %s);", (password, str(phone)))
        return True
    else:
        return False

# create_account(2376876, "dedeff")

# def allocated():
#
#
# def unallocated():


def new_errand(from_loc, to_loc, description, phone, price):
    # queryset.create(val=RawSQL("INSERT INTO ERRANDS VALUES ('%s', '%s', '1', '%s', '%s');", (from_loc, to_loc, str(phone), description)))
    # cursor.execute("INSERT INTO ERRANDS VALUES (" + str(from_loc) + "," + str(to_loc) + ", 1, '" + str(phone) + "','" + description + "'," + str(price) + ");")
    cursor.execute("INSERT INTO ERRANDS (from_loc, to_loc, status, phone, description, price) VALUES(%s, %s, '1', %s, %s, %s);", (str(from_loc), str(to_loc), description, str(phone), str(price)))
    cursor.execute("SELECT LAST_INSERT_ID();")
    return cursor.fetchone()[0]
    
#print(new_errand(4, 4, "efefff", 2376876, 432))

# def delete_errand(from_loc, to_loc, description, phone):
#     queryset.create(val=RawSQL("INSERT INTO ERRANDS VALUES ('%s', '%s', '1', '%s', '%s');", (from_loc, to_loc, str(phone), description)))
#     return True


# def display_errand():
#
#
# def authenticate():


# def my_errands():




# print(create_account(989898989898, "eiuwh"))



# cursor.execute("SHOW TABLES;")
# tables = cursor.fetchall()

connection.commit()

connection.close()
