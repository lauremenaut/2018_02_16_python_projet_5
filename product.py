#! /usr/bin/env phyton3
# coding: utf-8

""" Sets Product class.

Product class ...

"""

from config import database


class Product:
    """ Sets Product class.

    Consists of 5 methods :
        - __init__()
        - select_unhealthy_products_names()
        - select_healthy_products_information()
        - select_name_grade()
        - select_healthiest_match_information()

    """
    def __init__(self):
        """ Product constructor """
        pass

    def select_product_information(self, code):
        ''' Selects product information for product which product_id is
        given as a parameter (= code) '''
        product_information = database.query('''SELECT Product.product_id,
                                             Product.name,
                                             Product.description,
                                             Product.brand,
                                             Product.nutrition_grade
                                             FROM Product
                                             WHERE Product.product_id = :code''',
                                             code=code)
        return product_information

    def select_unhealthy_products_names(self, categorie):
        unhealthy_products = \
            database.query('''SELECT Product.name
                           FROM Product
                           JOIN Product_Categorie
                           ON Product.product_id = Product_Categorie.product_id
                           JOIN Categorie
                           ON Categorie.categorie_id = \
                               Product_Categorie.categorie_id
                           WHERE Categorie.name = :selected_categorie
                           AND (Product.nutrition_grade = 'e' OR \
                               Product.nutrition_grade = 'd')''',
                           selected_categorie=categorie)
        return unhealthy_products

    def select_healthy_products_information(self, categorie):
        # Retrieves products from chosen categorie which nutrition_grade is
        # "a" or "b"
        healthy_products = \
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
                           WHERE (Product.nutrition_grade = 'a' OR \
                               Product.nutrition_grade = 'b')
                           AND Categorie.name = :categorie''',
                           categorie=categorie)
        return healthy_products

    def select_match_information(self, match):
        healthy_match = database.query('''SELECT name, nutrition_grade
                                       FROM Product
                                       WHERE name = :name
                                       AND nutrition_grade = "a"''',
                                       name=match)
        return healthy_match

    def select_healthiest_match_information(self, healthiest_match):
        # Retrieves information for the product proposed to the user
        # ('healthiest_match')
        proposed_product = \
            database.query('''SELECT Product.product_id,
                                     Product.name,
                                     Product.description,
                                     Product.url
                           FROM Product
                           WHERE Product.name = :name''',
                           name=healthiest_match)
        return proposed_product

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


















