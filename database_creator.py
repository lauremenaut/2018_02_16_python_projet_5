#! /usr/bin/env python3
# coding: utf-8

""" Sets DatabaseCreator class.

DatabaseCreator class creates local database 'healthier_food'.

"""

from records import Database

import datetime

from params import MYSQL_ID, MYSQL_PW


class DatabaseCreator:
    """ Sets DatabaseCreator class.

    Consists of 5 private methods :
        - __init__()
        - _create_database()
        - _drop_foreign_keys()
        - _create_tables()
        - _create_foreign_keys()

    """
    def __init__(self):
        """ DatabaseCreator constructor """
        self._create_database()

    def _create_database(self):
        """ Creates local database if not already exists """

# Avant de pouvoir créer la base, il faut se connecter via root pour donner
# les droits à l'utilisateur 'lauredougui' sur cette nouvelle base.
# GRANT ALL PRIVILEGES ON healthier_food.* TO 'lauredougui'@'localhost';

        db_name_to_clean = "healthier_food_" + str(datetime.datetime.now())

        db_name = ""

        for char in db_name_to_clean:
            if char in ["-", " ", ".", ":"]:
                char = "_"
            db_name = db_name + char

        print("db_name: ", db_name)

        connexion = Database(f'mysql+pymysql://{MYSQL_ID}:\
{MYSQL_PW}@localhost/?charset=utf8')

        connexion.query(f'CREATE DATABASE {db_name} CHARACTER SET "utf8"')

        connexion.query(f'USE {db_name}')

        with open('db_name.txt', "w") as f:
            f.write(db_name)


def main():
    DatabaseCreator()


if __name__ == "__main__":
    main()
