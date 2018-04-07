#! /usr/bin/env python3
# coding: utf-8

""" Sets ProductCategoryManager class.

ProductCategoryManager class sets methods containing queries to
interact with ProductCategory table.
Imported in :
- app.py
- database_filler.py
- database_updater.py

"""


class ProductCategoryManager:

    """ Sets ProductCategoryManager class.

    Class consists of 6 methods :
        - __init__()
        - insert()
        - select_based_on_product_id()
        - select_based_on_product_name()
        - select_based_on_category_id()
        - delete()

    """

    def __init__(self, database):
        """ ProductCategoryManager constructor.

        Sets 'self.database' attribute.

        """
        self.database = database

    def insert(self, category, name):
        """ Manages insertion into Product_Category table.

        Adds Product / Category relationship (based on given category
        name and product name) into Product_Category table.
        Note : Unique Key prevents duplicate entry.

        """
        self.database.query('''INSERT IGNORE INTO
                            Product_Category (product_id, category_id)
                            VALUES ((SELECT product_id FROM Product
                                     WHERE name = :name),
                                    (SELECT category_id FROM Category
                                     WHERE name = :category))''',
                            name=name, category=category)
        print(f'La relation {name} / {category} a été ajoutée dans la table Product_Category !')

    def select_based_on_product_id(self, product_id):
        """ Manages selection of categories id based on product id.

        Returns selected categories id for given product id.

        """
        categories_id = \
            self.database.query('''SELECT Product_Category.category_id
                                FROM Product_Category
                                WHERE Product_Category.product_id = \
                                    :product_id''',
                                product_id=product_id)
        return categories_id

    def select_based_on_product_name(self, product_name):
        """ Manages selection of categories id based on product name.

        Returns selected categories id for given product name.

        """
        categories_id = \
            self.database.query('''SELECT Product_Category.category_id
                                FROM Product_Category
                                JOIN Product
                                ON Product.product_id = \
                                    Product_Category.product_id
                                WHERE Product.name = :name''',
                                name=product_name)
        return categories_id

    def select_based_on_category_id(self, category_id):
        """  Manages selection based on category id.

        Returns selected categories & products id for given category
        id.

        """
        product_category = \
            self.database.query('''SELECT Product_Category.category_id,
                                          Product_Category.product_id
                                FROM Product_Category
                                WHERE Product_Category.category_id = \
                                    :category_id''',
                                category_id=category_id)
        return product_category

    def delete(self, product_id, category_id):
        """ Manages removal from Product_Category table.

        Deletes Product / Category relationship from Product_Category
        table.

        """
        self.database.query('''DELETE FROM Product_Category
                            WHERE Product_Category.product_id = \
                                :product_id
                                AND Product_Category.category_id = \
                                :category_id''',
                            product_id=product_id,
                            category_id=category_id)
        print(f'La relation {product_id} / {category_id} a été supprimée de la table Product_Category !')
