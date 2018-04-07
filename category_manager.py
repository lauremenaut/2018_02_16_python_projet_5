#! /usr/bin/env python3
# coding: utf-8

""" Sets CategoryManager class.

CategoryManager class sets methods containing queries to interact with
CategoryManager table.
Imported in :
- database_filler.py
- database_updater.py

"""


class CategoryManager:

    """ Sets CategoryManager class.

    Class consists of 5 methods :
        - __init__()
        - insert()
        - select_based_on_id()
        - select_based_on_name()
        - delete()

    """

    def __init__(self, database):
        """ CategoryManager constructor.

        Sets 'self.database' attribute.

        """
        self.database = database

    def insert(self, category):
        """ Manages insertion of given category into Category table.

        Adds category name into Category table.
        Note : Unique Key on category name column prevents duplicate
        entry.

        """
        self.database.query('''INSERT IGNORE INTO Category (name)
                            VALUES (:category)''',
                            category=category)
        print(f'La category "{category}" a été ajoutée à la table Catégorie !')

    def select_based_on_id(self, category_id):
        """ Manages selection of category name.

        Returns selected category name based on given category id.

        """
        category = \
            self.database.query('''SELECT Category.name
                                FROM Category
                                WHERE Category.category_id = :category_id''',
                                category_id=category_id)
        return category[0]['name']

    def select_based_on_name(self, category):
        """ Manages selection of category name and id.

        Returns selected category information based on given category
        name.

        """
        category = \
            self.database.query('''SELECT Category.name,
                                          Category.category_id
                                FROM Category
                                WHERE Category.name = :category''',
                                category=category)
        return category

    def delete(self, category):
        """ Manages category removal.

        Deletes category from Category table based on given category
        name.

        """
        self.database.query('''DELETE FROM Category
                            WHERE Category.name = :category''',
                            category=category)
        print(f'La category "{category}" a été supprimée de la table Catégorie !')
