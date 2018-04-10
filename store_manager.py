#! /usr/bin/env python3
# coding: utf-8

""" Sets StoreManager class.

StoreManager class sets methods containing queries to interact with
Store table.
Imported in :
- app.py
- database_filler.py
- database_updater.py

"""


class StoreManager:

    """ Sets StoreManager class.

    Consists of 5 methods :
        - __init__()
        - insert()
        - select_store_based_on_id()
        - select_store_based_on_name()
        - delete()

    """

    def __init__(self, database):
        """ StoreManager constructor.

        Sets 'self.database' attribute.

        """
        self.database = database

    def insert(self, store):
        """ Manages insertion of given store into Store table.

        Adds store name into Store table.
        Note : Unique Key on store name column prevents duplicate entry.

        """
        self.database.query('''INSERT IGNORE INTO Store (name)
                            VALUES (:store)''', store=store)
        print(f'Le magasin "{store}" a été ajouté à la table Store !',
              file=open('print_log.txt', 'a'))

    def select_based_on_id(self, store_id):
        """ Manages selection of store name.

        Returns selected store name based on given store id.

        """
        store = self.database.query('''SELECT Store.name
                                    FROM Store
                                    WHERE Store.store_id = :store_id''',
                                    store_id=store_id)
        return store[0]['name']

    def select_based_on_name(self, store):
        """ Manages selection of store name and id.

        Returns selected store information based on given store name.

        """
        store = \
            self.database.query('''SELECT store.name,
                                          store.store_id
                                FROM store
                                WHERE store.name = :store''',
                                store=store)
        return store

    def delete(self, store):
        """ Manages store removal.

        Deletes store from Store table based on given store name.

        """
        self.database.query('''DELETE FROM store
                            WHERE store.name = :store''',
                            store=store)
        print(f'Le magasin "{store}" a été supprimé de la table Store !',
              file=open('print_log.txt', 'a'))
