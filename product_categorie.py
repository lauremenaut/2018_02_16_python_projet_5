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

    def select_product_categories_id(self, code):
        categories_id = \
            database.query('''SELECT Product_Categorie.categorie_id
                           FROM Product_Categorie
                           JOIN Product
                           ON Product.product_id = Product_Categorie.product_id
                           WHERE Product.product_id = :code''',
                           code=code)
        return categories_id

    def select_unhealthy_product_categories_id(self, unhealthy_product):
        # Retrieves id of categories to which belongs the chosen
        # unhealthy product
        unhealthy_product_categories_id = \
            database.query('''SELECT Product_Categorie.categorie_id
                           FROM Product_Categorie
                           JOIN Product
                           ON Product.product_id = Product_Categorie.product_id
                           WHERE Product.name = :name''',
                           name=unhealthy_product)
        return unhealthy_product_categories_id

    def select_healthy_product_categories_id(self, healthy_product_name):
        healthy_product_categories_ids = \
            database.query('''SELECT Product_Categorie.categorie_id
                           FROM Product_Categorie
                           JOIN Product
                           ON Product.product_id = \
                               Product_Categorie.product_id
                           WHERE Product.name = :name''',
                           name=healthy_product_name)
        return healthy_product_categories_ids
