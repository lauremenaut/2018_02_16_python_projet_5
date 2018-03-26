#! /usr/bin/env phyton3
# coding: utf-8

""" Sets DatabaseUpdater class.

DatabaseUpdater class updates information of each product one-by-one of
'healthier_food' database.

"""

from requests import get

import datetime  # A affiner

from config import database
from product import Product
from categorie import Categorie
from product_categorie import Product_Categorie

# Où met-on ces 2 lignes ??
# import sys
# OFF_product_keys = open('OFF_product_keys.txt', 'w')  # .txt non tracké (??)
# sys.stdout = OFF_product_keys


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
        # self.update_datetime = datetime.datetime.now()
        # print(f'Date de la dernière mise à jour : {self.update_datetime}')
        self._product_update()

    def _product_update(self):
        """ ... Open Food Facts API ... """

        # Retrieves product_ids for all products in local database
        codes = database.query('''SELECT Product.product_id
                FROM Product''')

        # for i in range(len(codes.all())):
        for i in range(4):
            try:  # Attention : gérer le cas où le produit a été retiré de la base !!
                # For each product_id, retrieves product information from OFF API
                response = get(f'''https://fr.openfoodfacts.org/api/v0/product/{codes[i]['product_id']}.json''')
                data = response.json()
                OFF_product = data['product']

                OFF_code = OFF_product['code']
                OFF_name = OFF_product['product_name'].strip().capitalize()
                OFF_description = OFF_product['generic_name'].capitalize()
                OFF_brands = (OFF_product['brands']).split(',')
                OFF_brand = OFF_brands[0].capitalize()
                OFF_categories_to_strip = (OFF_product['categories']).split(',')
                OFF_categories = []
                for categorie in OFF_categories_to_strip:
                    OFF_categories.append(categorie.strip().capitalize())
                OFF_stores_to_strip = (OFF_product['stores']).split(',')
                OFF_stores = []
                for store in OFF_stores_to_strip:
                    OFF_stores.append(store.strip().capitalize())
                OFF_nutrition_grade = OFF_product['nutrition_grades'].lower()

                local_product = Product.select_product_information(self, OFF_code)

                # print('\n\n', code, name, description)
                # print(local_product[0]['product_id'], local_product[0]['name'], local_product[0]['description'], '\n')

                if local_product[0]['name'] != OFF_name:
                    Product.update_name(OFF_name, OFF_code)
                    print('"name" updated !')
                if local_product[0]['description'] != OFF_description:
                    Product.update_description(OFF_description, OFF_code)
                    print('"description" updated !')
                if local_product[0]['brand'] != OFF_brand:
                    Product.update_brand(OFF_brand, OFF_code)
                    print('"brand" updated !')
                if local_product[0]['nutrition_grade'] != OFF_nutrition_grade:
                    Product.update_nutrition_grade(OFF_nutrition_grade, OFF_code)
                    print('"nutrition_grade" updated !')

                local_product_categories_id = Product_Categorie.select_product_categories_id(self, OFF_code)

                print('1 - local_product_categories_id.all() : ', local_product_categories_id.all())
                print('2 - len(local_product_categories_id) : ', len(local_product_categories_id.all()))

                local_product_categories_list = []

                for j in range(len(local_product_categories_id.all())):
                    categorie_name = Categorie.select_categorie_name(self, local_product_categories_id[j]['categorie_id'])
                    local_product_categories_list.append(categorie_name[0]['name'])

                for k in range(len(local_product_categories_list)):
                    if local_product_categories_list[k] not in OFF_categories:
                        Product_Categorie.delete_line(self, OFF_code, local_product_categories_id[k]['categorie_id'])
                        print(f'Removed corresponding line between product "{local_product[0]["name"]}" and categorie "{local_product_categories_list[k]}" from Product_Categorie table')
                # Vérifier si la catégorie est toujours utilisée, sinon on peut la supprimer de la table Categorie

                print('A - local_product_categories_list : ', local_product_categories_list)
                print('B - OFF_categories_list : ', OFF_categories)

                for categorie in OFF_categories:
                    if categorie not in local_product_categories_list:
                        pass
                        # 1 - si le nom existe déjà dans la table Categorie
                        # alors on récupère son id et on ajoute une ligne dans Product_Categorie
                        # 2 - sinon, on ajoute le nom dans Categorie, on récupère l'id et on ajoute une ligne dans Product_Categorie
                        # database.query('''INSERT INTO
                        #                Product_Categorie (product_id, categorie_id)
                        #                VALUES ((SELECT product_id FROM Product
                        #                         WHERE product_id = :code),
                        #                        (SELECT categorie_id FROM Categorie
                        #                         WHERE name = :categorie))''',
                        #                code=OFF_code, categorie=categorie)


                print('******************\nEnd of loop\n******************')

            except KeyError as e:
                print(e)


def main():
    DatabaseUpdater()


if __name__ == '__main__':
    main()
