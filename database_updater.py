#! /usr/bin/env phyton3
# coding: utf-8

""" Sets DatabaseUpdater class.

DatabaseUpdater class updates information of each product one-by-one of
'healthier_food' database.

"""

from requests import get

from time import time
import pickle
import sys

from config import database
from product import Product
from categorie import Categorie
from product_categorie import Product_Categorie
from store import Store
from product_store import Product_Store

# Où met-on ces 2 lignes ??
# errors_log_db_updater = open('errors_log_db_updater.txt', 'w')  # .txt non tracké (??)
# sys.stderr = errors_log_db_updater


class DatabaseUpdater:  # 'Old-style class defined' ??
    """ Sets DatabaseUpdater class.

    Consists of 2 methods :
        - __init__()
        - _product_update()

    """
    def __init__(self):
        """ DatabaseUpdater constructor.

        For each
        """
        self._product_update()
        last_update_date = time()

        with open('last_update', "wb") as f:
            my_pickler = pickle.Pickler(f)
            my_pickler.dump(last_update_date)

    def _product_update(self):
        """ ... Open Food Facts API ... """

        # Retrieves product_ids for all products in local database
        codes = database.query('''SELECT Product.product_id
                FROM Product''')

        # for i in range(len(codes.all())):
        for i in range(10):
            print('\n********Nouveau produit !*********')
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

                # print(OFF_code, OFF_name, OFF_description)  # A supprimer
                # print(local_product[0]['product_id'], local_product[0]['name'], local_product[0]['description'], '\n')  # A supprimer

                if local_product[0]['name'] != OFF_name:
                    Product.update_name(self, OFF_name, OFF_code)
                    print('"name" updated !')
                if local_product[0]['description'] != OFF_description:
                    Product.update_description(self, OFF_description, OFF_code)
                    print('"description" updated !')
                if local_product[0]['brand'] != OFF_brand:
                    Product.update_brand(self, OFF_brand, OFF_code)
                    print('"brand" updated !')
                if local_product[0]['nutrition_grade'] != OFF_nutrition_grade:
                    Product.update_nutrition_grade(self, OFF_nutrition_grade, OFF_code)
                    print('"nutrition_grade" updated !')

                local_product_categories_id = Product_Categorie.select_categories_id_based_on_product_id(self, OFF_code)

                local_product_categories_list = []

                # print('1 - local_product_categories_id.all() : ', local_product_categories_id.all())  # A supprimer
                # print('2 - len(local_product_categories_id) : ', len(local_product_categories_id.all()))  # A supprimer

                for j in range(len(local_product_categories_id.all())):
                    categorie_name = Categorie.select_categorie_name_based_on_id(self, local_product_categories_id[j]['categorie_id'])
                    local_product_categories_list.append(categorie_name[0]['name'])

                for k in range(len(local_product_categories_list)):
                    if local_product_categories_list[k] not in OFF_categories:
                        Product_Categorie.delete(self, OFF_code, local_product_categories_id[k]['categorie_id'])
                        print(f'Removed corresponding line between product "{local_product[0]["name"]}" and categorie "{local_product_categories_list[k]}" from Product_Categorie table')

                        product_categorie = Product_Categorie.select_product_categorie_based_on_categorie_id(self, local_product_categories_id[k]['categorie_id'])
                        try:
                            categorie_id = product_categorie[0]['categorie_id']
                            print('La categorie est associée à d\'autre(s) produit(s)')
                        except IndexError:
                            print('La categorie n\'est associée à aucun autre produit')
                            Categorie.delete(self, local_product_categories_list[k])

                # print('A - local_product_categories_list : ', local_product_categories_list)  # A supprimer
                # print('B - OFF_categories_list : ', OFF_categories)  # A supprimer

                for categorie in OFF_categories:
                    if categorie not in local_product_categories_list:
                        local_categorie = Categorie.select_categorie_name_based_on_name(self, categorie)
                        try:
                            local_categorie_name = local_categorie[0]['name']
                            Product_Categorie.insert(self, local_categorie_name, OFF_name)
                        except IndexError:
                            print('La catégorie n\'existe pas')
                            Categorie.insert(self, local_categorie_name)
                            Product_Categorie.insert(self, local_categorie_name, OFF_name)

                # print('******************\nEnd of loop\n******************')  # A supprimer

            except KeyError as e:
                print(e)


def main():
    DatabaseUpdater()


if __name__ == '__main__':
    main()
