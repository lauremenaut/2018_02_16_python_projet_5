#! /usr/bin/env python3
# coding: utf-8

""" Sets ProductManager class.

ProductManager class sets methods containing queries to interact with
Product table.
Imported in :
- app.py
- database_filler.py
- database_updater.py

"""


class ProductManager:

    """ Sets ProductManager class.

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

    def __init__(self, database):
        """ ProductManager constructor.

        Sets 'self.database' attribute.

        """
        self.database = database

    def insert(self, code, name, description, brand, url, nutrition_grade):
        """ Manages insertion of given information into Product table.

        Adds product information (i.e. code, name, description, brand,
        url & nutrition_grade) into Product table.
        Note : 'code' is saved as 'product_id'.

        """
        self.database.query('''INSERT IGNORE INTO Product
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
        """ Manages selection of product information.

        Returns selected product information for given code
        (product_id).

        """
        product_information = \
            self.database.query('''SELECT Product.product_id,
                                          Product.name,
                                          Product.description,
                                          Product.brand,
                                          Product.nutrition_grade
                                FROM Product
                                WHERE Product.product_id = :code''',
                                code=code)
        return product_information

    def select_products_information(self, category, n_g_1, n_g_2):
        """ Manages selection of product information.

        Returns selected products information for given category &
        nutrition grades.

        """
        products_information = \
            self.database.query('''SELECT Product.product_id,
                                          Product.name,
                                          Product.description,
                                          Product.url
                                FROM Product
                                JOIN Product_Category
                                ON Product.product_id = \
                                   Product_Category.product_id
                                JOIN Category
                                ON Category.category_id = \
                                   Product_Category.category_id
                                WHERE Category.name = :category
                                    AND (Product.nutrition_grade = :n_g_1 OR \
                                         Product.nutrition_grade = :n_g_2)''',
                                category=category,
                                n_g_1=n_g_1,
                                n_g_2=n_g_2)
        return products_information

    def select_match_information(self, name):
        """ Manages selection of product information.

        Returns selected product name for given product name &
        nutrition grade = 'a'.

        """
        product_name = \
            self.database.query('''SELECT Product.name
                                FROM Product
                                WHERE name = :name
                                    AND nutrition_grade = "a"''',
                                name=name)
        return product_name

    def select_healthiest_match_information(self, name):
        """ Manages selection of product information.

        Returns selected product information for given product name.

        """
        product_information = \
            self.database.query('''SELECT Product.product_id,
                                          Product.name,
                                          Product.description,
                                          Product.url
                                FROM Product
                                WHERE Product.name = :name''',
                                name=name)
        return product_information

    def update_name(self, name, code):
        """ Manages product name update.

        Updates product name for given product code.

        """
        self.database.query('''UPDATE IGNORE Product
                            SET name = :name
                            WHERE Product.product_id = :code''',
                            name=name, code=code)

    def update_description(self, description, code):
        """ Manages product description update.

        Updates product description for given product code.

        """
        self.database.query('''UPDATE IGNORE Product
                            SET description = :description
                            WHERE Product.product_id = :code''',
                            description=description, code=code)

    def update_brand(self, brand, code):
        """ Manages product brand update.

        Updates product brand for given product code.

        """
        self.database.query('''UPDATE IGNORE Product
                            SET brand = :brand
                            WHERE Product.product_id = :code''',
                            brand=brand, code=code)

    def update_nutrition_grade(self, nutrition_grade, code):
        """ Manages product nutrition grade update.

        Updates product nutrition grade for given product code.

        """
        self.database.query('''UPDATE IGNORE Product
                            SET nutrition_grade = :nutrition_grade
                            WHERE Product.product_id = :code''',
                            nutrition_grade=nutrition_grade, code=code)
