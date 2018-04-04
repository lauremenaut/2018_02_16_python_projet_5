#! /usr/bin/env python3
# coding: utf-8

""" Contains configuration data """

from records import Database

from params import MYSQL_ID, MYSQL_PW

with open('db_name.txt', "r") as f:
    db_name = f.read()

database = Database(f'''mysql+pymysql://{MYSQL_ID}:\
{MYSQL_PW}@localhost/{db_name}?charset=utf8''')
