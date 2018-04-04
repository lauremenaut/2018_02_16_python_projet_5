#! /usr/bin/env python3
# coding: utf-8

""" Sets ProductCategorieManager class.

ProductCategorieManager class ...

"""

from database import database


class ProductCategorieManager:
    """ Sets ProductCategorieManager class.

    Class consists of 5 methods :
        - insert()
        - select_based_on_product_id()
        - select_based_on_product_name()
        - select_based_on_categorie_id()
        - delete()

    """
    def insert(self, categorie, name):
        """ Adds Product / Categorie relationship into Product_Categorie
        table
        Note : Unique Key prevents duplicate entry

        """
        database.query('''INSERT IGNORE INTO
                       Product_Categorie (product_id, categorie_id)
                       VALUES ((SELECT product_id FROM Product
                                WHERE name = :name),
                               (SELECT categorie_id FROM Categorie
                                WHERE name = :categorie))''',
                       name=name, categorie=categorie)
        print(f'La relation {name} / {categorie} a été ajoutée dans la table Product_Categorie !')

    def select_based_on_product_id(self, product_id):
        """ Returns selected categories id for given product id """
        categories_id = \
            database.query('''SELECT Product_Categorie.categorie_id
                           FROM Product_Categorie
                           WHERE Product_Categorie.product_id = :product_id''',
                           product_id=product_id)
        return categories_id

    def select_based_on_product_name(self, product_name):
        """ Returns selected categories id for given product name """
        categories_id = \
            database.query('''SELECT Product_Categorie.categorie_id
                           FROM Product_Categorie
                           JOIN Product
                           ON Product.product_id = Product_Categorie.product_id
                           WHERE Product.name = :name''',
                           name=product_name)
        return categories_id

    def select_based_on_categorie_id(self, categorie_id):
        """ Returns selected categories & products id for given categorie id """
        product_categorie = \
            database.query('''SELECT Product_Categorie.categorie_id,
                                     Product_Categorie.product_id
                           FROM Product_Categorie
                           WHERE Product_Categorie.categorie_id = :categorie_id''',
                           categorie_id=categorie_id)
        return product_categorie

    def delete(self, product_id, categorie_id):
        """ Deletes Product / Categorie relationship from
        Product_Categorie table

        """
        database.query('''DELETE FROM Product_Categorie
                       WHERE Product_Categorie.product_id = :product_id
                           AND Product_Categorie.categorie_id = :categorie_id''',
                       product_id=product_id,
                       categorie_id=categorie_id)
        print(f'La relation {product_id} / {categorie_id} a été supprimée de la table Product_Categorie !')
