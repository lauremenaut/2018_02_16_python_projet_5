#! /usr/bin/env python3
# coding: utf-8

""" Sets StoreManager class.

StoreManager class ...

"""

from database import database


class StoreManager:
    """ Sets StoreManager class.

    Class consists of 4 methods :
        - insert()
        - select_store_based_on_id()
        - select_store_based_on_name()
        - delete()

    """
    def insert(self, store):
        """ Adds store name into Store table
        Note : Unique Key on store name column prevents duplicate entry

        """
        database.query('''INSERT IGNORE INTO Store (name)
                       VALUES (:store)''', store=store)
        print(f'Le magasin "{store}" a été ajouté à la table Store !')

    def select_based_on_id(self, store_id):
        """ Returns selected store name for given store_id """
        store = database.query('''SELECT Store.name
                               FROM Store
                               WHERE Store.store_id = :store_id''',
                               store_id=store_id)
        return store[0]['name']

    def select_based_on_name(self, store):
        """ Returns selected store information for given store name """
        store = \
            database.query('''SELECT store.name,
                                     store.store_id
                           FROM store
                           WHERE store.name = :store''',
                           store=store)
        return store

    def delete(self, store):
        """ Deletes store from Store table """
        database.query('''DELETE FROM store
                       WHERE store.name = :store''',
                       store=store)
        print(f'Le magasin "{store}" a été supprimé de la table Store !')
