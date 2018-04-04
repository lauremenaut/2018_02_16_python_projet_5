#! /usr/bin/env python3
# coding: utf-8

""" Sets CategorieManager class.

CategorieManager class ...

"""

from database import database


class CategorieManager:
    """ Sets CategorieManager class.

    Class consists of 4 methods :
        - insert()
        - select_based_on_id()
        - select_based_on_name()
        - delete()

    """
    def insert(self, categorie):
        """ Adds categorie name into Categorie table
        Note : Unique Key on categorie name column prevents duplicate
        entry

        """
        database.query('''INSERT IGNORE INTO Categorie (name)
                       VALUES (:categorie)''',
                       categorie=categorie)
        print(f'La categorie "{categorie}" a été ajoutée à la table Catégorie !')

    def select_based_on_id(self, categorie_id):
        """ Returns selected categorie name for given categorie_id """
        categorie = \
            database.query('''SELECT Categorie.name
                           FROM Categorie
                           WHERE Categorie.categorie_id = :categorie_id''',
                           categorie_id=categorie_id)
        return categorie[0]['name']

    def select_based_on_name(self, categorie):
        """ Returns selected categorie information for given categorie
        name

        """
        categorie = \
            database.query('''SELECT Categorie.name,
                                     Categorie.categorie_id
                           FROM Categorie
                           WHERE Categorie.name = :categorie''',
                           categorie=categorie)
        return categorie

    def delete(self, categorie):
        """ Deletes categorie from Categorie table """
        database.query('''DELETE FROM Categorie
                       WHERE Categorie.name = :categorie''',
                       categorie=categorie)
        print(f'La categorie "{categorie}" a été supprimée de la table Catégorie !')
