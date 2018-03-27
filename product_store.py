#! /usr/bin/env phyton3
# coding: utf-8

""" Sets Product_Store class.

Product_Store class ...

"""

from config import database


class Product_Store:
    """ Sets Product_Store class.

    Class consists of 3 methods :
        - __init__()
        - insert()
        - select_store_ids

    """
    def __init__(self):
        """ Product_Store constructor """
        pass

    def insert(self, store, name):
        # Store information is added in Store and
        # Product_Store tables (Unique Key on store name column
        # prevents duplicate entry)
            database.query('''INSERT IGNORE INTO
                           Product_Store (product_id, store_id)
                           VALUES ((SELECT product_id FROM Product
                                    WHERE name = :name),
                                   (SELECT store_id FROM Store
                                    WHERE name = :store))''',
                           name=name, store=store)

    def select_stores_id(self, name):
        store_ids = database.query('''SELECT Product_Store.store_id
                                   FROM Product_Store
                                   JOIN Product
                                   ON Product.product_id = \
                                       Product_Store.product_id
                                   WHERE Product.name = :name''',
                                   name=name)
        return store_ids
