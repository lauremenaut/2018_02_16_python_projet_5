#! /usr/bin/env phyton3
# coding: utf-8

""" Contains configuration data """

from records import Database

import datetime

from untracked_config import mysql_id, mysql_pw


# db_name = "healthier_food_" + str(datetime.datetime.now())
# Problème de droits d'accès à la base !
db_name = "healthier_food"

# database = Database(f'mysql+pymysql://{mysql_id}:{mysql_pw}@localhost')
database = Database(f'''mysql+pymysql://{mysql_id}:{mysql_pw}@localhost/
    {db_name}?charset=utf8''')

nutrition_grades = ["a", "b", "d", "e"]

tag_categories = ["Sodas", "Viennoiseries", "Biscuits secs", "Crèmes glacées",
                  "Céréales au chocolat", "Pizzas"]
