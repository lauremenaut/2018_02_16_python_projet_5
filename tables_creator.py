#! /usr/bin/env python3
# coding: utf-8

""" Sets TablesCreator class.

TablesCreator class creates empty tables and related foreign keys in
local MySQL database.

"""

from config import database_connection


class TablesCreator:

    """ Sets TablesCreator class.

    Consists of 3 private methods :
        - __init__()
        - _create_tables()
        - _create_foreign_keys()

    """

    def __init__(self, database):
        """ TablesCreator constructor.

        Runs _create_tables() & _create_foreign_keys() methods.

        """
        self._create_tables(database)
        self._create_foreign_keys(database)

    def _create_tables(self, database):
        """ Manages tables creation.

        Creates 6 empty tables :
        - Product
        - Category
        - Product_Category
        - Store
        - Product_Store
        - History

        """
        database.query('''CREATE TABLE Product (
                       product_id BIGINT UNSIGNED NOT NULL,
                       name VARCHAR(100) UNIQUE NOT NULL,
                       description TEXT(500) NOT NULL,
                       brand VARCHAR(30) UNIQUE NOT NULL,
                       url VARCHAR(150) NOT NULL,
                       nutrition_grade CHAR(1) NOT NULL,
                       PRIMARY KEY (product_id))''')

        database.query('''CREATE TABLE Category (
                       category_id SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
                       name VARCHAR(150) UNIQUE NOT NULL,
                       PRIMARY KEY (category_id))''')

        database.query('''CREATE TABLE Product_Category (
                       product_id BIGINT UNSIGNED NOT NULL,
                       category_id SMALLINT UNSIGNED NOT NULL,
                       PRIMARY KEY (product_id, category_id))''')

        database.query('''CREATE TABLE Store (
                       store_id SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
                       name VARCHAR(50) UNIQUE NOT NULL,
                       PRIMARY KEY (store_id))''')

        database.query('''CREATE TABLE Product_Store (
                       product_id BIGINT UNSIGNED NOT NULL,
                       store_id SMALLINT UNSIGNED NOT NULL,
                       PRIMARY KEY (product_id, store_id))''')

        database.query('''CREATE TABLE History (
                       history_id INT UNSIGNED AUTO_INCREMENT NOT NULL,
                       request_date DATETIME NOT NULL,
                       unhealthy_product VARCHAR(100) NOT NULL,
                       healthy_product VARCHAR(100) NOT NULL,
                       description TEXT(500) NOT NULL,
                       stores VARCHAR(100) NOT NULL,
                       url VARCHAR(150) NOT NULL,
                       PRIMARY KEY (history_id))''')

    def _create_foreign_keys(self, database):
        """ Manages foreign keys creation.

        Creates foreign keys managing many-to-many relationships
        between :
            - Product & Product_Category tables
            - Category & Product_Category tables
            - Product & Product_Store tables
            - Store & Product_Store tables

        """
        database.query('''ALTER TABLE Product_Category
                       ADD CONSTRAINT product_product_category_fk
                       FOREIGN KEY (product_id)
                       REFERENCES Product (product_id)
                       ON DELETE NO ACTION
                       ON UPDATE NO ACTION''')

        database.query('''ALTER TABLE Product_Category
                       ADD CONSTRAINT category_product_category_fk
                       FOREIGN KEY (category_id)
                       REFERENCES Category (category_id)
                       ON DELETE NO ACTION
                       ON UPDATE NO ACTION''')

        database.query('''ALTER TABLE Product_Store
                       ADD CONSTRAINT product_product_store_fk
                       FOREIGN KEY (product_id)
                       REFERENCES Product (product_id)
                       ON DELETE NO ACTION
                       ON UPDATE NO ACTION''')

        database.query('''ALTER TABLE Product_Store
                       ADD CONSTRAINT store_product_store_fk
                       FOREIGN KEY (store_id)
                       REFERENCES Store (store_id)
                       ON DELETE NO ACTION
                       ON UPDATE NO ACTION''')


def main():
    database = database_connection()
    TablesCreator(database)


if __name__ == "__main__":
    main()
