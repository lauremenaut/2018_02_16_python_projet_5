#! /usr/bin/env phyton3
# coding: utf-8

""" Sets DB_Creator class.

Creator class creates a new database called "healthier_food".

"""

import records


class DB_Creator:
    """ Sets DB_Creator class """
    def __init__(self):
        """ DB_Creator constructor """

        #  La base doit déjà exister pour pouvoir s'y connecter ... un peu paradoxal pour une classe de création :-/

        #  Est-ce que je laisse tout dans la méthode __init__ ... ?

        self.db = records.Database('mysql+pymysql://lauredougui:mysql@localhost/healthier_food?charset=utf8')

        self.db.query('DROP DATABASE IF EXISTS healthier_food')
        self.db.query('CREATE DATABASE healthier_food CHARACTER SET "utf8"')
        self.db.query('USE healthier_food')

        self.db.query('''CREATE TABLE Product (
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

        self.db.query('''CREATE TABLE Store (
                        store_id SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
                        name VARCHAR(50) UNIQUE NOT NULL,
                        PRIMARY KEY (store_id))''')

        self.db.query('''CREATE TABLE Categorie (
                        categorie_id SMALLINT UNSIGNED AUTO_INCREMENT NOT NULL,
                        name VARCHAR(150) UNIQUE NOT NULL,
                        PRIMARY KEY (categorie_id))''')

        self.db.query('''CREATE TABLE Product_Categorie (
                        product_id INT UNSIGNED NOT NULL,
                        categorie_id SMALLINT UNSIGNED NOT NULL,
                        PRIMARY KEY (product_id, categorie_id))''')

        self.db.query('''CREATE TABLE History (
                        history_id INT UNSIGNED AUTO_INCREMENT NOT NULL,
                        request_date DATE NOT NULL,
                        healthy_product_id INT NOT NULL,
                        bad_product_id INT NOT NULL,
                        PRIMARY KEY (history_id))''')

        self.db.query('''ALTER TABLE Product ADD CONSTRAINT store_product_fk
        FOREIGN KEY (store_id)
        REFERENCES Store (store_id)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION''')

        self.db.query('''ALTER TABLE Product_Categorie ADD CONSTRAINT product_product_categorie_fk
        FOREIGN KEY (product_id)
        REFERENCES Product (product_id)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION''')

        self.db.query('''ALTER TABLE Product_Categorie ADD CONSTRAINT categorie_product_categorie_fk
        FOREIGN KEY (categorie_id)
        REFERENCES Categorie (categorie_id)
        ON DELETE NO ACTION
        ON UPDATE NO ACTION''')


def main():
    healthier_food = DB_Creator()


if __name__ == "__main__":
    main()
