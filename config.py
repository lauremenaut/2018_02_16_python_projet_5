#! /usr/bin/env python3
# coding: utf-8

""" Contains configuration data """

from records import Database

import datetime

from params import MYSQL_ID, MYSQL_PW


# db_name = "healthier_food_" + str(datetime.datetime.now())
# Problème de droits d'accès à la base !
db_name = "healthier_food"

# database = Database(f'mysql+pymysql://{MYSQL_ID}:{MYSQL_PW}@localhost/?charset=utf8')
database = Database(f'''mysql+pymysql://{MYSQL_ID}:\
{MYSQL_PW}@localhost/{db_name}?charset=utf8''')

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
