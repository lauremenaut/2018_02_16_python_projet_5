#! /usr/bin/env python3
# coding: utf-8

""" Sets CategorieManager class.

CategorieManager class sets methods containing queries to interact with
CategorieManager table.

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
        """ Manages insertion of given categorie into Categorie table.

        Adds categorie name into Categorie table.
        Note : Unique Key on categorie name column prevents duplicate
        entry.

        """
        database.query('''INSERT IGNORE INTO Categorie (name)
                       VALUES (:categorie)''',
                       categorie=categorie)
        print(f'La categorie "{categorie}" a été ajoutée à la table Catégorie !')

    def select_based_on_id(self, categorie_id):
        """ Manages selection of categorie name.

        Returns selected categorie name based on given categorie id.

        """
        categorie = \
            database.query('''SELECT Categorie.name
                           FROM Categorie
                           WHERE Categorie.categorie_id = :categorie_id''',
                           categorie_id=categorie_id)
        return categorie[0]['name']

    def select_based_on_name(self, categorie):
        """ Manages selection of categorie name and id.

        Returns selected categorie information based on given categorie
        name.

        """
        categorie = \
            database.query('''SELECT Categorie.name,
                                     Categorie.categorie_id
                           FROM Categorie
                           WHERE Categorie.name = :categorie''',
                           categorie=categorie)
        return categorie

    def delete(self, categorie):
        """ Manages categorie removal.

        Deletes categorie from Categorie table based on given categorie
        name.

        """
        database.query('''DELETE FROM Categorie
                       WHERE Categorie.name = :categorie''',
                       categorie=categorie)
        print(f'La categorie "{categorie}" a été supprimée de la table Catégorie !')
