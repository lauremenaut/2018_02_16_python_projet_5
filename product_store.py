#! /usr/bin/env phyton3
# coding: utf-8

""" Sets Product_Store class.

Product_Store class ...

"""

from config import database


class Product_Store:
    """ Sets Product_Store class.

    Class consists of 2 methods :
        - __init__()
        - select_store_ids

    """
    def __init__(self):
        """ Product_Store constructor """
        pass

    def select_store_ids(self, healthiest_match):
        store_ids = database.query('''SELECT Product_Store.store_id
                                   FROM Product_Store
                                   JOIN Product
                                   ON Product.product_id = \
                                       Product_Store.product_id
                                   WHERE Product.name = :name''',
                                   name=healthiest_match)
        return store_ids
