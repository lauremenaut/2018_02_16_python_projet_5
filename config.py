#! /usr/bin/env python3
# coding: utf-8

""" Configuration data.

    Sets database_connection() method.
    Contains tags for requests criteria.
    Imported in :
    - app.py
    - tables_creator.py
    - database_filler.py
    - database_updater.py

"""

from records import Database

from params import MYSQL_ID, MYSQL_PW


def database_connection():
    """ Manages connection to the database.

    Opens 'db_name.txt' to retrieve db_name.
    Connects to MySQL local database via records.Database
    Returns 'database' object containing connection with database.

    """
    with open('db_name.txt', "r") as f:
        db_name = f.read()

    database = Database(f'''mysql+pymysql://{MYSQL_ID}:{MYSQL_PW}@localhost/\
{db_name}?charset=utf8''')

    return database

# Tags for nutrition grades of healthy and unhealthy products
nutrition_grades = ["a", "b", "d", "e"]

# Tags for (unhealthy) products categories
tag_categories = ["Céréales pour petit-déjeuner",
                  "Pizzas",
                  "Plats préparés",
                  "Produits laitiers",
                  "Crèmes dessert",
                  "Fromages",
                  "Snacks sucrés",
                  "Confiseries",
                  "Sodas"
                  ]
