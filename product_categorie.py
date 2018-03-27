#! /usr/bin/env phyton3
# coding: utf-8

""" Sets Product_Categorie class.

Product_Categorie class ...

"""

from config import database


class Product_Categorie:
    """ Sets Product_Categorie class.

    Class consists of 3 methods :
        - __init__()
        - select_unhealthy_product_categories_id()
        - select_healthy_product_categories_id()

    """
    def __init__(self):
        """ Product_Categorie constructor """
        pass

    def select_categories_id_based_on_product_id(self, product_id):
        categories_id = \
            database.query('''SELECT Product_Categorie.categorie_id
                           FROM Product_Categorie
                           WHERE Product_Categorie.product_id = :product_id''',
                           product_id=product_id)
        return categories_id

    def select_categories_id_based_on_product_name(self, product_name):
        # Retrieves id of categories to which belongs the chosen
        # unhealthy product
        categories_id = \
            database.query('''SELECT Product_Categorie.categorie_id
                           FROM Product_Categorie
                           JOIN Product
                           ON Product.product_id = Product_Categorie.product_id
                           WHERE Product.name = :name''',
                           name=product_name)
        return categories_id

    def delete_line(self, product_id, categorie_id):
        database.query('''DELETE FROM Product_Categorie
                       WHERE Product_Categorie.product_id = :product_id
                           AND Product_Categorie.categorie_id = :categorie_id''',
                       product_id=product_id,
                       categorie_id=categorie_id)
