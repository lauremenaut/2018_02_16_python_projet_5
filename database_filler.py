#! /usr/bin/env phyton3
# coding: utf-8

""" Sets DatabaseFiller class.

DatabaseFiller class fills 'healthier_food' database, connecting with Open
Food Facts API.

"""

from requests import get

from config import database, db_name, nutrition_grades, tag_categories


class DatabaseFiller:  # 'Old-style class defined' ??
    """ Sets DatabaseFiller class.

    Consists of 3 methods :
        - __init__()
        - get_products()
        - fill_db()

    """
    def __init__(self):
        """ DatabaseFiller constructor.

        For each categorie and for each nutrition grade, retrieves
        corresponding products from Open Food Facts API and adds them to
        local database.

        """
        for nutrition_grade in nutrition_grades:
            for categorie in tag_categories:
                products = self.get_products(categorie, nutrition_grade)
                self.fill_db(products)

    def get_products(self, categorie, nutrition_grade):  # 'Method could be a function (no-self-used)' ??
        """ Gets products from Open Food Facts API following given
        criteria. """
        criteria = {
            "action": "process",
            "json": 1,
            "countries": "France",
            "page_size": 20,
            "page": 1,
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": categorie,
            "tagtype_1": "nutrition_grades",
            "tag_contains_1": "contains",
            "tag_1": nutrition_grade
            }

        response = get('https://fr.openfoodfacts.org/cgi/search.pl',
                       params=criteria)
        data = response.json()

        # 'products' is a list of dictionnaries
        products = data["products"]
        return products

    def fill_db(self, products):  # 'Method could be a function (no-self-used)' ??
        """ Contains SQL requests to fill database """
        # database.query('SET NAMES "utf8"')
        # database.query(f'USE {db_name}')

        # For each product, checks if required data is available or not
        for product in products:
            try:
                code = product["code"]
                name = product["product_name"].strip().capitalize()
                description = product["generic_name"].capitalize()
                brands = (product["brands"]).split(",")
                brand = brands[0].capitalize()
                url = product["url"]
                categories_to_strip = (product["categories"]).split(",")
                categories = []
                for categorie in categories_to_strip:
                    categories.append(categorie.strip().capitalize())
                stores_to_strip = (product["stores"]).split(",")
                stores = []
                for store in stores_to_strip:
                    stores.append(store.strip().capitalize())
                nutrition_grade = product["nutrition_grades"].lower()

            except KeyError:
                print("Missing data")

            # If required data is available, product is added to local
            # database
            if all([code, name, description, brand, url,
                    nutrition_grade, categories[0], stores[0]]):
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

                # Categorie information is added in Categorie and
                # Product_Categorie tables (Unique Key on categorie name
                # column prevents duplicate entry)
                for categorie in categories:
                    database.query('''INSERT IGNORE INTO Categorie (name)
                                   VALUES (:categorie)''',
                                   categorie=categorie)

                    database.query('''INSERT IGNORE INTO
                                   Product_Categorie (product_id, categorie_id)
                                   VALUES ((SELECT product_id FROM Product
                                            WHERE name = :name),
                                           (SELECT categorie_id FROM Categorie
                                            WHERE name = :categorie))''',
                                   name=name, categorie=categorie)

                # Store information is added in Store and
                # Product_Store tables (Unique Key on store name column
                # prevents duplicate entry)
                for store in stores:
                    database.query('''INSERT IGNORE INTO Store (name)
                                   VALUES (:store)''', store=store)

                    database.query('''INSERT IGNORE INTO
                                   Product_Store (product_id, store_id)
                                   VALUES ((SELECT product_id FROM Product
                                            WHERE name = :name),
                                           (SELECT store_id FROM Store
                                            WHERE name = :store))''',
                                   name=name, store=store)


def main():
    DatabaseFiller()


if __name__ == "__main__":
    main()
