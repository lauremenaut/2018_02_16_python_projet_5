#! /usr/bin/env phyton3
# coding: utf-8

""" Sets DatabaseUpdater class.

DatabaseUpdater class updates information of each product one-by-one of
'healthier_food' database.

"""

from requests import get

from config import database


class DatabaseUpdater:  # 'Old-style class defined' ??
    """ Sets DatabaseUpdater class.

    Consists of * methods :
        - __init__()
        - g

    """
    def __init__(self):
        """ DatabaseUpdater constructor.

        For each
        """
        self.product_update()

    def product_update(self):
        """ ... Open Food Facts API ... """
        codes = database.query('''SELECT Product.product_id
                FROM Product''')

        for i in range(100):  # A adapter au nombre de produits tant que pas de solution pour connaitre la longueur de l'objet 'codes' ...
            try:
                response = get(f'''https://fr.openfoodfacts.org/api/v0/product/{codes[i]["product_id"]}.json''')
                data = response.json()
                OFF_product = data["product"]

                code = OFF_product["code"]
                name = OFF_product["product_name"].strip().capitalize()
                description = OFF_product["generic_name"].capitalize()
                brands = (OFF_product["brands"]).split(",")
                brand = brands[0].capitalize()
                # url = OFF_product["url"]
                # print(url)
                categories_to_strip = (OFF_product["categories"]).split(",")
                categories = []
                for categorie in categories_to_strip:
                    categories.append(categorie.strip().capitalize())
                stores_to_strip = (OFF_product["stores"]).split(",")
                stores = []
                for store in stores_to_strip:
                    stores.append(store.strip().capitalize())
                nutrition_grade = OFF_product["nutrition_grades"].lower()


                local_product = database.query('''SELECT Product.product_id,
                                                         Product.name,
                                                         Product.description,
                                                         Product.brand,
                                                         -- Product.url,
                                                         Product.nutriscore
                                               FROM Product
                                               WHERE Product.product_id = :code''',
                                               code=code)

                print("\n\n", code, name, description)
                print(local_product[0]["product_id"], local_product[0]["name"], local_product[0]["description"], "\n")

                if local_product[0]["name"] != name:
                    database.query('''UPDATE IGNORE Product SET name = :name''', name=name)
                    print("'name' updated !")
                # Problème dans la mise à jour de la description, décalage + 1 ...
                if local_product[0]["description"] != description:
                    database.query('''UPDATE IGNORE Product SET description = :description''', description=description)
                    print("'description' updated !")
                if local_product[0]["brand"] != brand:
                    database.query('''UPDATE IGNORE Product SET brand = :brand''', brand=brand)
                    print("'brand' updated !")
                # if local_product[0]["url"] != url:
                #     database.query('''UPDATE IGNORE Product SET url = :url''', url=url)
                #     print("'name' updated !")
                if local_product[0]["nutriscore"] != nutrition_grade:
                    database.query('''UPDATE IGNORE Product SET nutrition_grade = :nutrition_grade''', nutrition_grade=nutrition_grade)
                    print("'nutriscore' updated !")

                # local_product_categories = \
                #     database.query('''SELECT Categorie.name
                #                    FROM Categorie
                #                    JOIN Product_Categorie
                #                    ON Categorie.categorie_id = Product_Categorie.categorie_id
                #                    WHERE Categorie.categorie_id = (SELECT Product_Categorie.categorie_id,
                #                                                    FROM Product_Categorie
                #                                                    JOIN Product
                #                                                    ON Product.product_id = Product_Categorie.product_id
                #                                                    WHERE Product.product_id = :code)''',
                #                    code=code)

                # local_product_categories_list = []

                # try:
                #     for i in range(10):
                #         local_product_categories_list. \
                #             append(local_product_categories[i]["name"])

                #         if local_product_categories_list[i] not in categories:
                #             database.query('''DELETE FROM Product_Categorie
                #                            WHERE Product_Categorie.product_id = :code''',
                #                            code=code)
                # except IndexError:
                #     pass

                # for categorie in categories:
                #     if categorie not in local_product_categories_list:
                #         database.query('''INSERT INTO
                #                        Product_Categorie (product_id, categorie_id)
                #                        VALUES ((SELECT product_id FROM Product
                #                                 WHERE product_id = :code),
                #                                (SELECT categorie_id FROM Categorie
                #                                 WHERE name = :categorie))''',
                #                        code=code, categorie=categorie)

            except IndexError as e:
                print(e)
            except KeyError as e:
                print(e)


def main():
    DatabaseUpdater()


if __name__ == "__main__":
    main()
