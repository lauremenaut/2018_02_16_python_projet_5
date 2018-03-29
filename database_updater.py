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

    Consists of 7 methods :
        - __init__()
        - _get_products_codes()
        - _get_OFF_product()
        - _update_new_information()
        - _update_categories_information()
        - _update_store_information()
        - _save_update_date()

    """
    def __init__(self):
        """ DatabaseUpdater constructor.

        For each
        """

        # Retrieves product code for each product in local database
        codes = self._get_products_codes()

        # for i in range(len(codes.all())):
        for i in range(20):
            print('\n********Nouveau produit !*********')  # A supprimer !
            try:  # Attention : gérer le cas où le produit a été retiré de la base !!
                self._get_OFF_product(codes, i)
                local_product = \
                    Product.select_product_information(self, self.OFF_code)
                self._update_new_information(local_product)
                self._update_categories_information(local_product)
                self._update_store_information()
            except KeyError as e:
                print('Aïe, KeyError : ', e)

        # self._save_update_date()

    def _get_products_codes(self):

        codes = database.query('''SELECT Product.product_id FROM Product''')
        return codes

    def _get_OFF_product(self, codes, i):
        # For each product code, retrieves product information from OFF API
        response = get(f'''https://fr.openfoodfacts.org/api/v0/product/{codes[i]['product_id']}.json''')
        data = response.json()
        OFF_product = data['product']

        self.OFF_code = OFF_product['code']
        self.OFF_name = OFF_product['product_name'].strip().capitalize()
        self.OFF_description = OFF_product['generic_name'].capitalize()
        OFF_brands = (OFF_product['brands']).split(',')
        self.OFF_brand = OFF_brands[0].capitalize()
        OFF_categories_to_strip = (OFF_product['categories']).split(',')
        self.OFF_categories = []
        for categorie in OFF_categories_to_strip:
            self.OFF_categories.append(categorie.strip().capitalize())
        OFF_stores_to_strip = (OFF_product['stores']).split(',')
        self.OFF_stores = []
        for store in OFF_stores_to_strip:
            self.OFF_stores.append(store.strip().capitalize())
        self.OFF_nutrition_grade = OFF_product['nutrition_grades'].lower()

    def _update_new_information(self, local_product):

        if local_product[0]['name'] != self.OFF_name:
            Product.update_name(self, self.OFF_name, self.OFF_code)
            print('"name" updated !')
        if local_product[0]['description'] != self.OFF_description:
            Product.update_description(self, self.OFF_description, self.OFF_code)
            print('"description" updated !')
        if local_product[0]['brand'] != self.OFF_brand:
            Product.update_brand(self, self.OFF_brand, self.OFF_code)
            print('"brand" updated !')
        if local_product[0]['nutrition_grade'] != self.OFF_nutrition_grade:
            Product.update_nutrition_grade(self, self.OFF_nutrition_grade, self.OFF_code)
            print('"nutrition_grade" updated !')

    def _update_categories_information(self, local_product):

        local_product_categories_id, local_product_categories_list = self._make_local_product_categories_list()
        self._remove_obsolete_categories(local_product, local_product_categories_id, local_product_categories_list)
        self._add_new_categories(local_product_categories_list)


        # print('A - local_product_categories_list : ', local_product_categories_list)  # A supprimer
        # print('B - OFF_categories_list : ', OFF_categories)  # A supprimer


    def _make_local_product_categories_list(self):

        local_product_categories_id = Product_Categorie.select_categories_id_based_on_product_id(self, self.OFF_code)

        local_product_categories_list = []

        # print('1 - local_product_categories_id.all() : ', local_product_categories_id.all())  # A supprimer
        # print('2 - len(local_product_categories_id) : ', len(local_product_categories_id.all()))  # A supprimer

        for i in range(len(local_product_categories_id.all())):
            categorie_name = Categorie.select_categorie_name_based_on_id(self, local_product_categories_id[i]['categorie_id'])
            local_product_categories_list.append(categorie_name[0]['name'])

        return local_product_categories_id, local_product_categories_list

    def _remove_obsolete_categories(self, local_product, local_product_categories_id, local_product_categories_list):

        for i in range(len(local_product_categories_list)):
            if local_product_categories_list[i] not in self.OFF_categories:
                Product_Categorie.delete(self, self.OFF_code, local_product_categories_id[i]['categorie_id'])
                print(f'Removed corresponding line between product "{local_product[0]["name"]}" and categorie "{local_product_categories_list[i]}" from Product_Categorie table')

                product_categorie = Product_Categorie.select_product_categorie_based_on_categorie_id(self, local_product_categories_id[i]['categorie_id'])
                try:
                    categorie_id = product_categorie[0]['categorie_id']
                    print('La categorie est associée à d\'autre(s) produit(s)')
                except IndexError:
                    print('La categorie n\'est associée à aucun autre produit')
                    Categorie.delete(self, local_product_categories_list[i])

    def _add_new_categories(self, local_product_categories_list):

        for categorie in self.OFF_categories:
            if categorie not in local_product_categories_list:
                local_categorie = Categorie.select_categorie_name_based_on_name(self, categorie)
                try:
                    local_categorie_name = local_categorie[0]['name']
                    Product_Categorie.insert(self, local_categorie_name, self.OFF_name)
                except IndexError:
                    print('La catégorie n\'existe pas')
                    Categorie.insert(self, local_categorie_name)
                    Product_Categorie.insert(self, local_categorie_name, self.OFF_name)

    def _update_store_information(self):
        pass
        # To do !

    def _save_update_date(self):
        last_update_date = time()

        with open('last_update', "wb") as f:
            my_pickler = pickle.Pickler(f)
            my_pickler.dump(last_update_date)


def main():
    DatabaseUpdater()


if __name__ == '__main__':
    main()
