#! /usr/bin/env phyton3
# coding: utf-8

""" Sets Product class.

Product class ...

"""

from config import database


class Product:
    """ Sets Product class.

    Consists of 10 methods :
        - __init__()
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
    def __init__(self):
        """ Product constructor """
        pass

    def insert(self, code, name, description, brand, url, nutrition_grade):
        # Product information is added in Product table
        # 'code' is saved in 'product_id' column
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
        ''' Selects product information for product which product_id is
        given as a parameter (= code) '''
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

# Peut-on combiner ces 2 méthodes ?? Comment mettre n_g en paramètre ...
    def select_match_information(self, name):
        product_information = \
            database.query('''SELECT Product.name
                           FROM Product
                           WHERE name = :name
                           AND nutrition_grade = "a"''',
                           name=name)
        return product_information

    def select_healthiest_match_information(self, name):
        # Retrieves information for the product proposed to the user
        # ('healthiest_match')
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
        database.query('''UPDATE IGNORE Product
                       SET name = :name
                       WHERE Product.product_id = :code''',
                       name=name, code=code)

    def update_description(self, description, code):
        database.query('''UPDATE IGNORE Product
                       SET description = :description
                       WHERE Product.product_id = :code''',
                       description=description, code=code)

    def update_brand(self, brand, code):
        database.query('''UPDATE IGNORE Product
                       SET brand = :brand
                       WHERE Product.product_id = :code''',
                       brand=brand, code=code)

    def update_nutrition_grade(self, nutrition_grade, code):
        database.query('''UPDATE IGNORE Product
                       SET nutrition_grade = :nutrition_grade
                       WHERE Product.product_id = :code''',
                       nutrition_grade=nutrition_grade, code=code)
