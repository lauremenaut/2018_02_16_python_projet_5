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
        -

    """
    def __init__(self):
        """ Categorie constructor """
        pass

    def select_categorie_name(self, categorie_id):
        categorie_name = \
            database.query('''SELECT Categorie.name
                           FROM Categorie
                           JOIN Product_Categorie
                           ON Categorie.categorie_id = Product_Categorie.categorie_id
                           WHERE Categorie.categorie_id = :categorie_id''',
                           categorie_id=categorie_id)
        return categorie_name
