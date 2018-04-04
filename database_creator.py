#! /usr/bin/env python3
# coding: utf-8

""" Sets DatabaseCreator class.

DatabaseCreator class creates a local database with MySQL.

"""

from datetime import datetime

from records import Database

from params import MYSQL_ID, MYSQL_PW


class DatabaseCreator:

    """ Sets DatabaseCreator class.

    Consists of 3 private methods :
        - __init__()
        - _create_database()
        - _set_db_name()

    """

    def __init__(self):
        """ DatabaseCreator constructor.

        Sets db_name variable and runs _create_database() method.

        """
        db_name = self._set_db_name()
        self._create_database(db_name)

    def _set_db_name(self):
        """ Sets name for MySQL database.

        Returns a cleaned unique name for MySQL database (based on
        datetime.now()).
        Writes database name in an external .txt file.

        """
        db_name_to_clean = "healthier_food_" + str(datetime.now())

        db_name = ""

        # Replaces all punctuation marks contained in datetime string
        # by '_' (avoiding failure of database creation due to invalid
        # database name)
        for char in db_name_to_clean:
            if char in ["-", " ", ".", ":"]:
                char = "_"
            db_name = db_name + char

        print("db_name: ", db_name)  # A supprimer

        with open('db_name.txt', "w") as f:
            f.write(db_name)

        return db_name

    def _create_database(self, db_name):
        """ Manages database creation.

        Connects to MySQL via Database class from records library.
        Creates a new MySQL local database.
        Selects this new database for use.

        """
        connexion = Database(f'mysql+pymysql://{MYSQL_ID}:\
{MYSQL_PW}@localhost/?charset=utf8')

        connexion.query(f'CREATE DATABASE {db_name} CHARACTER SET "utf8"')

        connexion.query(f'USE {db_name}')

def main():
    DatabaseCreator()


if __name__ == "__main__":
    main()
