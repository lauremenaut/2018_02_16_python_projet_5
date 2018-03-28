#! /usr/bin/env phyton3
# coding: utf-8

""" Sets DatabaseCreator class.

DatabaseCreator class creates local database 'healthier_food'.

"""

from config import database, db_name


class DatabaseCreator:
    """ Sets DatabaseCreator class.

    Consists of 5 private methods :
        - __init__()
        - _create_database()
        - _drop_foreign_keys()
        - _create_tables()
        - _create_foreign_keys()

    """
    def __init__(self):
        """ DatabaseCreator constructor """
        self._create_database()
        self._drop_foreign_keys()
        self._create_tables()
        self._create_foreign_keys()

    def _create_database(self):
        """ Creates local database if not already exists """

# Avant de pouvoir créer la base, il faut se connecter via root pour donner
# les droits à l'utilisateur 'lauredougui' sur cette nouvelle base.
# GRANT ALL PRIVILEGES ON healthier_food.* TO 'lauredougui'@'localhost';

        # database.query(f'DROP DATABASE IF EXISTS {db_name}')
        # database.query(f'CREATE DATABASE {db_name} CHARACTER SET "utf8"')
        database.query(f"""CREATE DATABASE IF NOT EXISTS {db_name}
                       CHARACTER SET 'utf8'""")
        database.query(f'USE {db_name}')

    def _drop_foreign_keys(self):
        """ Deletes foreign keys if exist """
        try:
            database.query('''ALTER TABLE Product_Categorie
                           DROP FOREIGN KEY product_product_categorie_fk''')
            database.query('''ALTER TABLE Product_Categorie
                           DROP FOREIGN KEY categorie_product_categorie_fk''')
            database.query('''ALTER TABLE Product_Store
                           DROP FOREIGN KEY product_product_store_fk''')
            database.query('''ALTER TABLE Product_Store
                           DROP FOREIGN KEY store_product_store_fk''')
        except:  # Comment améliorer ça ?
            print('Foreign keys not dropped')

    def _create_tables(self):
        """ Creates or recreates empty tables, except for History table
        which content is not dropped """
        database.query('DROP TABLE IF EXISTS Product')
        database.query('''CREATE TABLE Product (
                       product_id BIGINT UNSIGNED NOT NULL,
                       name VARCHAR(100) UNIQUE NOT NULL,
                       description TEXT(500) NOT NULL,
                       brand VARCHAR(30) UNIQUE NOT NULL,
                       url VARCHAR(150) NOT NULL,
                       nutrition_grade CHAR(1) NOT NULL,
                       PRIMARY KEY (product_id))''')

        database.query('DROP TABLE IF EXISTS Categorie')
        database.query('''CREATE TABLE Categorie (
                       categorie_id SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
                       name VARCHAR(150) UNIQUE NOT NULL,
                       PRIMARY KEY (categorie_id))''')

        database.query('DROP TABLE IF EXISTS Product_Categorie')
        database.query('''CREATE TABLE Product_Categorie (
                       product_id BIGINT UNSIGNED NOT NULL,
                       categorie_id SMALLINT UNSIGNED NOT NULL,
                       PRIMARY KEY (product_id, categorie_id))''')

        database.query('DROP TABLE IF EXISTS Store')
        database.query('''CREATE TABLE Store (
                       store_id SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
                       name VARCHAR(50) UNIQUE NOT NULL,
                       PRIMARY KEY (store_id))''')

        database.query('DROP TABLE IF EXISTS Product_Store')
        database.query('''CREATE TABLE Product_Store (
                       product_id BIGINT UNSIGNED NOT NULL,
                       store_id SMALLINT UNSIGNED NOT NULL,
                       PRIMARY KEY (product_id, store_id))''')

        database.query('''CREATE TABLE IF NOT EXISTS History (
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
    DatabaseCreator()


if __name__ == "__main__":
    main()
