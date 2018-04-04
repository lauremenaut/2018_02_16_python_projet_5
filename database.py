#! /usr/bin/env python3
# coding: utf-8

""" Sets 'database' variable, connecting Python script with MySQL.
Called by tables_creator.py, database_updater.py & all table manager
files

"""

from records import Database

from params import MYSQL_ID, MYSQL_PW

with open('db_name.txt', "r") as f:
    db_name = f.read()

database = Database(f'''mysql+pymysql://{MYSQL_ID}:{MYSQL_PW}@localhost/\
{db_name}?charset=utf8''')
