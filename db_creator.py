#! /usr/bin/env phyton3
# coding: utf-8

""" Sets DB_Creator class.

Creator class creates a new database called 'healthier_food'.

"""

from config import database


class DB_Creator:
    """ Sets DB_Creator class """
    def __init__(self):
        """ DB_Creator constructor """
        self.create_database()
        self.create_tables()
        self.create_foreign_keys()

        #  La base doit déjà exister pour pouvoir s'y connecter ... un peu paradoxal pour une classe de création :-/

    def create_database(self):
        """ Manages database creation """
        database.query('DROP DATABASE IF EXISTS healthier_food')
        database.query('CREATE DATABASE healthier_food CHARACTER SET "utf8"')
        database.query('USE healthier_food')

    def create_tables(self):
        """ Manages tables creation """
        database.query('''CREATE TABLE Product (
                        product_id INT UNSIGNED AUTO_INCREMENT NOT NULL,
                        name VARCHAR(100) UNIQUE NOT NULL,
                        description VARCHAR(100) NOT NULL,
                        brand VARCHAR(30) UNIQUE NOT NULL,
                        url VARCHAR(150) NOT NULL,
                        store_id SMALLINT UNSIGNED,
                        nutriscore CHAR(1) NOT NULL,
                        ingredients VARCHAR(500),
                        energy_100g VARCHAR(5),
                        allergens VARCHAR(300),
                        traces VARCHAR(200),
                        additives VARCHAR(300),
                        labels VARCHAR(150),
                        PRIMARY KEY (product_id))''')

        database.query('''CREATE TABLE Store (
                        store_id SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
                        name VARCHAR(50) UNIQUE NOT NULL,
                        PRIMARY KEY (store_id))''')

        database.query('''CREATE TABLE Categorie (
                        categorie_id SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
                        name VARCHAR(150) UNIQUE NOT NULL,
                        PRIMARY KEY (categorie_id))''')

        database.query('''CREATE TABLE Product_Categorie (
                        product_id INT UNSIGNED NOT NULL,
                        categorie_id SMALLINT UNSIGNED NOT NULL,
                        PRIMARY KEY (product_id, categorie_id))''')

        database.query('''CREATE TABLE History (
                        history_id INT UNSIGNED AUTO_INCREMENT NOT NULL,
                        request_date DATETIME,
                        unhealthy_product VARCHAR(100),
                        healthy_product VARCHAR(100),
                        description VARCHAR(100),
                        store VARCHAR(50),
                        url VARCHAR(150),
                        PRIMARY KEY (history_id))''')

    def create_foreign_keys(self):
        """ Manages foreign keys creation """
        database.query('''ALTER TABLE Product ADD CONSTRAINT store_product_fk
        FOREIGN KEY (store_id)
        REFERENCES Store (store_id)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION''')

        database.query('''ALTER TABLE Product_Categorie ADD CONSTRAINT product_product_categorie_fk
        FOREIGN KEY (product_id)
        REFERENCES Product (product_id)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION''')

        database.query('''ALTER TABLE Product_Categorie ADD CONSTRAINT categorie_product_categorie_fk
        FOREIGN KEY (categorie_id)
        REFERENCES Categorie (categorie_id)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION''')


def main():
    DB_Creator()


if __name__ == "__main__":
    main()
