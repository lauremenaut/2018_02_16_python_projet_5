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

    def select_categorie_name_based_on_id(self, categorie_id):
        categorie_name = \
            database.query('''SELECT Categorie.name
                           FROM Categorie
                           WHERE Categorie.categorie_id = :categorie_id''',
                           categorie_id=categorie_id)
        return categorie_name

    def select_categorie_name_based_on_name(self, name):
        categorie_name = \
            database.query('''SELECT Categorie.name
                           FROM Categorie
                           WHERE Categorie.name = :name''',
                           name=name)
        return categorie_name
