#! /usr/bin/env phyton3
# coding: utf-8

""" Sets Store class.

Store class ...

"""

from config import database


class Store:
    """ Sets Store class.

    Class consists of 3 methods :
        - __init__()
        - insert()
        - select_store()

    """
    def __init__(self):
        """ Store constructor """
        pass

    def insert(self, store):
        # Store information is added in Store and
        # Product_Store tables (Unique Key on store name column
        # prevents duplicate entry)
            database.query('''INSERT IGNORE INTO Store (name)
                           VALUES (:store)''', store=store)

    def select(self, store_id):
        store = database.query('''SELECT Store.name
                               FROM Store
                               WHERE Store.store_id = :store_id''',
                               store_id=store_id)
        return store[0]['name']
