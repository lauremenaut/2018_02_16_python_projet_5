#! /usr/bin/env python3
# coding: utf-8

""" Contains configuration data """

from records import Database

from params import MYSQL_ID, MYSQL_PW

import datetime
# db_name = "healthier_food_" + str(datetime.datetime.now())


db_name_to_clean = "healthier_food_" + str(datetime.datetime.now())

db_name_now = ""

for char in db_name_to_clean:
    if char in ["-", " ", ".", ":"]:
        char = "_"
    db_name_now = db_name_now + char

print("db_name 1: ", db_name_now)


# db_name = "healthier_food"

connexion = Database(f'mysql+pymysql://{MYSQL_ID}:\
{MYSQL_PW}@localhost/?charset=utf8')


connexion.query(f'CREATE DATABASE IF NOT EXISTS {db_name_now} CHARACTER SET "utf8"')

connexion.query(f'USE {db_name_now}')


db_name_steady = connexion.query(f'SELECT DATABASE()')
print("db_name_steady: ", db_name_steady[0]["DATABASE()"])


database = Database(f'''mysql+pymysql://{MYSQL_ID}:\
{MYSQL_PW}@localhost/{db_name_steady[0]["DATABASE()"]}?charset=utf8''')

# Tags for nutrition_grades of healthy and unhealthy products
nutrition_grades = ["a", "b", "d", "e"]

# Tags for (unhealthy) products categories
tag_categories = ["Pizzas",
                  "Céréales pour petit-déjeuner",
                  "Snacks sucrés",
                  "Confiseries",
                  "Sodas",
                  "Plats préparés",
                  "Produits laitiers",
                  "Produits à tartiner",
                  "Fromages"
                  ]
