#! /usr/bin/env phyton3
# coding: utf-8

""" Sets Categorie class.

Categorie class ...

"""

from config import database


class Categorie:
    """ Sets Categorie class.

    Class consists of ... methods :
        - __init__()
        - insert()
        - select_categorie_name_based_on_id()
        - select_categorie_name_based_on_name()
        - delete()

    """
    def __init__(self):
        """ Categorie constructor """
        pass

    def insert(self, categorie):
        # Categorie information is added in Categorie and
        # Product_Categorie tables (Unique Key on categorie name
        # column prevents duplicate entry)
            database.query('''INSERT IGNORE INTO Categorie (name)
                           VALUES (:categorie)''',
                           categorie=categorie)

    def select_categorie_name_based_on_id(self, categorie_id):
        categorie_name = \
            database.query('''SELECT Categorie.name
                           FROM Categorie
                           WHERE Categorie.categorie_id = :categorie_id''',
                           categorie_id=categorie_id)
        return categorie_name

    def select_categorie_name_based_on_name(self, categorie):
        categorie_name = \
            database.query('''SELECT Categorie.name,
                                     Categorie.categorie_id
                           FROM Categorie
                           WHERE Categorie.name = :categorie''',
                           categorie=categorie)
        return categorie_name

    def delete(self, categorie):
        database.query('''DELETE FROM Categorie
                       WHERE Categorie.name = :categorie''',
                       categorie=categorie)
