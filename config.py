#! /usr/bin/env phyton3
# coding: utf-8

""" Contains configuration data """

from records import Database
import datetime

# les identifiants devraient être dans un fichier séparé, ignoré par Git
mysql_id = "lauredougui"
mysql_pw = "mysql"

# db_name = "healthier_food_" + str(datetime.datetime.now()) Problème de droits d'accès à la base !
db_name = "healthier_food"

# database = Database(f'mysql+pymysql://{mysql_id}:{mysql_pw}@localhost')
database = Database(f'mysql+pymysql://{mysql_id}:{mysql_pw}@localhost/{db_name}?charset=utf8')

nutrition_grades = ["a", "b", "d", "e"]

categories = ["Boissons sucrées", "Pains", "Biscuits", "Desserts", "Céréales au chocolat"]
