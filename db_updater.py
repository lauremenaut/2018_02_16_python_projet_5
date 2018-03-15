#! /usr/bin/env phyton3
# coding: utf-8

""" Sets DB_Updater class.

DB_Updater class fills "healthier_food" database, connecting with Open Food Facts API.

"""

from requests import get

from config import database, db_name, nutrition_grades, categories

class DB_Updater:
    """ Sets DB_Updater class """
    def __init__(self):
        """ DB_Updater constructor """
        for self.nutrition_grade in nutrition_grades:
            for self.categorie in categories:
                self.products = self.get_products()
                self.fill_db(self.products)

    def get_products(self):
        """ Gets products from Open Food Facts API. """
        criteria = {
            "action": "process",
            "json": 1,
            "countries": "France",
            "page_size": 100,
            "page": 1,
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": self.categorie,
            "tagtype_1": "nutrition_grades",
            "tag_contains_1": "contains",
            "tag_1": self.nutrition_grade
            }

        response = get('https://fr.openfoodfacts.org/cgi/search.pl', params=criteria)
        data = response.json()
        products = data["products"]  # products est une liste de dictionnaires correspondant aux produits de la page 1
        return products

    def fill_db(self, products):
        """ Contains SQL requests to fill database """
        # database.query('SET NAMES "utf8"')
        # database.query(f'USE {db_name}')
        for product in products:
            try:
                categories = product["categories"]
                name = product["product_name"]
                description = product["generic_name"]
                brands = (product["brands"]).split(",")
                brand = brands[0]
                url = product["url"]
                stores = (product["stores"]).split(",")
                store = stores[0]
                nutrition_grade = product["nutrition_grades"]
                allergens = product["allergens"]
                traces = product["traces"]
                labels = product["labels"]

            except KeyError:
                print("Missing data")

            if all([categories, name, description, brand, url, store, nutrition_grade]):
                database.query("""INSERT IGNORE INTO Product (name, description, brand, url, nutriscore, allergens, traces, labels)
                    VALUES (:name, :description, :brand, :url, :nutrition_grade, :allergens, :traces, :labels)""",
                               name=name, description=description, brand=brand, url=url, nutrition_grade=nutrition_grade, allergens=allergens, traces=traces, labels=labels)

                database.query('INSERT IGNORE INTO Store (name) VALUES (:store)', store=store)

                for categorie in categories.split(","):
                    database.query('INSERT IGNORE INTO Categorie (name) VALUES (:categorie)', categorie=categorie)

                    database.query("""INSERT IGNORE INTO Product_Categorie (product_id, categorie_id) VALUES
                        ((SELECT product_id FROM Product WHERE name = :name),
                        (SELECT categorie_id FROM Categorie WHERE name = :categorie))""", name=name, categorie=categorie)

                database.query("""UPDATE Product SET store_id =
                    (SELECT store_id FROM Store WHERE name = :store)
                    WHERE name = :name""", store=store, name=name)

        print(len(self.products))


def main():
    DB_Updater()


if __name__ == "__main__":
    main()
