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

    def select_product_categories(self, id):
        local_product_categories = \
            database.query('''SELECT Categorie.name
                           FROM Categorie
                           JOIN Product_Categorie
                           ON Categorie.categorie_id = Product_Categorie.categorie_id
                           WHERE Categorie.categorie_id = :id''',
                           id=id)
        return local_product_categories
