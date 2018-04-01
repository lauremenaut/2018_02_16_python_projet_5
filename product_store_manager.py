#! /usr/bin/env python3
# coding: utf-8

""" Sets ProductStoreManager class.

ProductStoreManager class ...

"""

from config import database


class ProductStoreManager:
    """ Sets ProductStoreManager class.

    Class consists of 5 methods :
        - insert()
        - select_based_on_product_id()
        - select_based_on_product_name()
        - select_based_on_store_id()
        - delete()

    """
    def insert(self, store, name):
        """ Adds Product / Store relationship into Product_Store
        table
        Note : Unique Key prevents duplicate entry

        """
        database.query('''INSERT IGNORE INTO
                       Product_Store (product_id, store_id)
                       VALUES ((SELECT product_id FROM Product
                                WHERE name = :name),
                               (SELECT store_id FROM Store
                                WHERE name = :store))''',
                       name=name, store=store)
        print(f'La relation {name} / {store} a été ajoutée dans la table Product_Store !')

    def select_based_on_product_id(self, product_id):
        """ Returns selected stores id for given product id """
        stores_id = \
            database.query('''SELECT Product_store.store_id
                           FROM Product_store
                           WHERE Product_store.product_id = :product_id''',
                           product_id=product_id)
        return stores_id

    def select_based_on_product_name(self, product_name):
        """ Returns selected stores id for given product name """
        stores_id = database.query('''SELECT Product_Store.store_id
                                   FROM Product_Store
                                   JOIN Product
                                   ON Product.product_id = \
                                       Product_Store.product_id
                                   WHERE Product.name = :name''',
                                   name=product_name)
        return stores_id

    def select_based_on_store_id(self, store_id):
        """ Returns selected stores & products id for given store id """
        product_store = \
            database.query('''SELECT Product_store.store_id,
                                     Product_store.product_id
                           FROM Product_store
                           WHERE Product_store.store_id = :store_id''',
                           store_id=store_id)
        return product_store

    def delete(self, product_id, store_id):
        """ Deletes Product / Store relationship from
        Product_Store table

        """
        database.query('''DELETE FROM Product_store
                       WHERE Product_store.product_id = :product_id
                           AND Product_store.store_id = :store_id''',
                       product_id=product_id,
                       store_id=store_id)
        print(f'La relation {product_id} / {store_id} a été supprimée de la table Product_Store !')
