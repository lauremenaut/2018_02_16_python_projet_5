#! /usr/bin/env python3
# coding: utf-8

""" Sets ProductManager class.

ProductManager class ...

"""

from database import database


class ProductManager:
    """ Sets ProductManager class.

    Consists of 9 methods :
        - insert()
        - select_product_information()
        - select_products_information()
        - select_match_information()
        - select_healthiest_match_information()
        - update_name()
        - update_description()
        - update_brand()
        - update_nutrition_grade()

    """

    def insert(self, code, name, description, brand, url, nutrition_grade):
        """ Adds product information into Product table
        Note : 'code' is saved as 'product_id'

        """
        database.query('''INSERT IGNORE INTO Product
               VALUES (:code,
                       :name,
                       :description,
                       :brand,
                       :url,
                       :nutrition_grade)''',
                       code=code,
                       name=name,
                       description=description,
                       brand=brand,
                       url=url,
                       nutrition_grade=nutrition_grade)

    def select_product_information(self, code):
        """ Returns selected product information for given code (/product_id) """
        product_information = \
            database.query('''SELECT Product.product_id,
                                     Product.name,
                                     Product.description,
                                     Product.brand,
                                     Product.nutrition_grade
                           FROM Product
                           WHERE Product.product_id = :code''',
                           code=code)
        return product_information

    def select_products_information(self, categorie, n_g_1, n_g_2):
        """ Returns selected products information for given categorie & nutrition
        grades

        """
        products_information = \
            database.query('''SELECT Product.product_id,
                                     Product.name,
                                     Product.description,
                                     Product.url
                           FROM Product
                           JOIN Product_Categorie
                           ON Product.product_id = Product_Categorie.product_id
                           JOIN Categorie
                           ON Categorie.categorie_id = \
                               Product_Categorie.categorie_id
                           WHERE Categorie.name = :categorie
                           AND (Product.nutrition_grade = :n_g_1 OR \
                               Product.nutrition_grade = :n_g_2)''',
                           categorie=categorie,
                           n_g_1=n_g_1,
                           n_g_2=n_g_2)
        return products_information

    def select_match_information(self, name):
        """ Returns selected product name for given product name & nutrition
        grade = 'a'

        """
        product_name = \
            database.query('''SELECT Product.name
                           FROM Product
                           WHERE name = :name
                           AND nutrition_grade = "a"''',
                           name=name)
        return product_name

    def select_healthiest_match_information(self, name):
        """ Returns selected product information for given product name """
        product_information = \
            database.query('''SELECT Product.product_id,
                                     Product.name,
                                     Product.description,
                                     Product.url
                           FROM Product
                           WHERE Product.name = :name''',
                           name=name)
        return product_information

    def update_name(self, name, code):
        """ Updates product name for given product code """
        database.query('''UPDATE IGNORE Product
                       SET name = :name
                       WHERE Product.product_id = :code''',
                       name=name, code=code)

    def update_description(self, description, code):
        """ Updates product description for given product code """
        database.query('''UPDATE IGNORE Product
                       SET description = :description
                       WHERE Product.product_id = :code''',
                       description=description, code=code)

    def update_brand(self, brand, code):
        """ Updates product brand for given product code """
        database.query('''UPDATE IGNORE Product
                       SET brand = :brand
                       WHERE Product.product_id = :code''',
                       brand=brand, code=code)

    def update_nutrition_grade(self, nutrition_grade, code):
        """ Updates product nutrition grade for given product code """
        database.query('''UPDATE IGNORE Product
                       SET nutrition_grade = :nutrition_grade
                       WHERE Product.product_id = :code''',
                       nutrition_grade=nutrition_grade, code=code)
