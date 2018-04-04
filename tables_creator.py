#! /usr/bin/env python3
# coding: utf-8

""" Sets TablesCreator class.

TablesCreator class creates ...

"""

from database import database


class TablesCreator:
    """ Sets TablesCreator class.

    Consists of 3 private methods :
        - __init__()
        - _create_tables()
        - _create_foreign_keys()

    """
    def __init__(self):
        """ TablesCreator constructor """
        self._create_tables()
        self._create_foreign_keys()

    def _create_tables(self):
        """ Creates empty tables """
        database.query('''CREATE TABLE Product (
                       product_id BIGINT UNSIGNED NOT NULL,
                       name VARCHAR(100) UNIQUE NOT NULL,
                       description TEXT(500) NOT NULL,
                       brand VARCHAR(30) UNIQUE NOT NULL,
                       url VARCHAR(150) NOT NULL,
                       nutrition_grade CHAR(1) NOT NULL,
                       PRIMARY KEY (product_id))''')

        database.query('''CREATE TABLE Categorie (
                       categorie_id SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
                       name VARCHAR(150) UNIQUE NOT NULL,
                       PRIMARY KEY (categorie_id))''')

        database.query('''CREATE TABLE Product_Categorie (
                       product_id BIGINT UNSIGNED NOT NULL,
                       categorie_id SMALLINT UNSIGNED NOT NULL,
                       PRIMARY KEY (product_id, categorie_id))''')

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

    def _create_foreign_keys(self):
        """ Creates or recreates foreign keys """
        database.query('''ALTER TABLE Product_Categorie
                       ADD CONSTRAINT product_product_categorie_fk
                       FOREIGN KEY (product_id)
                       REFERENCES Product (product_id)
                       ON DELETE NO ACTION
                       ON UPDATE NO ACTION''')

        database.query('''ALTER TABLE Product_Categorie
                       ADD CONSTRAINT categorie_product_categorie_fk
                       FOREIGN KEY (categorie_id)
                       REFERENCES Categorie (categorie_id)
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
    TablesCreator()


if __name__ == "__main__":
    main()
