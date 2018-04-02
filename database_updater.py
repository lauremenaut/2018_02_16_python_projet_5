#! /usr/bin/env python3
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
from product_manager import ProductManager
from categorie_manager import CategorieManager
from product_categorie_manager import ProductCategorieManager
from store_manager import StoreManager
from product_store_manager import ProductStoreManager

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
        self.product_manager = ProductManager()
        self.categorie_manager = CategorieManager()
        self.product_categorie_manager = ProductCategorieManager()
        self.store_manager = StoreManager()
        self.product_store_manager = ProductStoreManager()
        # Retrieves product code for each product in local database
        codes = self._get_products_codes()

        for i in range(len(codes.all())):
        # for i in range(100):
            print('\n********Nouveau produit !*********')  # A supprimer !
            try:  # Attention : gérer le cas où le produit a été retiré de la base !!
                self._get_OFF_product(codes, i)
                local_product = self.product_manager.select_product_information(self.OFF_code)
                self._update_new_information(local_product)
                self._update_categories_information(local_product)
                self._update_store_information(local_product)
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

        print(self.OFF_name)

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
            self.product_manager.update_name(self.OFF_name, self.OFF_code)
            print('"name" updated !')
        if local_product[0]['description'] != self.OFF_description:
            self.product_manager.update_description(self.OFF_description, self.OFF_code)
            print('"description" updated !')
        if local_product[0]['brand'] != self.OFF_brand:
            self.product_manager.update_brand(self.OFF_brand, self.OFF_code)
            print('"brand" updated !')
        if local_product[0]['nutrition_grade'] != self.OFF_nutrition_grade:
            self.product_manager.update_nutrition_grade(self.OFF_nutrition_grade, self.OFF_code)
            print('"nutrition_grade" updated !')

    def _update_categories_information(self, local_product):

        local_product_categories_id, local_product_categories_list = self._make_local_product_categories_list()

        print('A - Catégorie(s) enregistrée(s) en local : ', local_product_categories_list)  # A supprimer
        print('B - Catégorie(s) récupérée(s) sur OFF : ', self.OFF_categories)  # A supprimer

        self._remove_obsolete_categories(local_product, local_product_categories_id, local_product_categories_list)
        self._add_new_categories(local_product_categories_list)

    def _make_local_product_categories_list(self):

        local_product_categories_id = self.product_categorie_manager.select_based_on_product_id(self.OFF_code)

        local_product_categories_list = []

        # print('1 - local_product_categories_id.all() : ', local_product_categories_id.all())  # A supprimer
        # print('2 - len(local_product_categories_id) : ', len(local_product_categories_id.all()))  # A supprimer

        for i in range(len(local_product_categories_id.all())):
            categorie_name = self.categorie_manager.select_based_on_id(local_product_categories_id[i]['categorie_id'])
            local_product_categories_list.append(categorie_name)

        return local_product_categories_id, local_product_categories_list

    def _remove_obsolete_categories(self, local_product, local_product_categories_id, local_product_categories_list):

        for i in range(len(local_product_categories_list)):
            if local_product_categories_list[i] not in self.OFF_categories:
                self.product_categorie_manager.delete(self.OFF_code, local_product_categories_id[i]['categorie_id'])

                product_categorie = self.product_categorie_manager.select_based_on_categorie_id(local_product_categories_id[i]['categorie_id'])
                try:
                    categorie_id = product_categorie[0]['categorie_id']
                    print(f'La categorie {categorie_id} est associée à d\'autre(s) produit(s). On la conserve.')
                except IndexError:
                    # print(f'La categorie {categorie_id} n\'est associée à aucun autre produit. On la supprime')
                    print('La categorie n\'est associée à aucun autre produit. On la supprime')
                    self.categorie_manager.delete(local_product_categories_list[i])

    def _add_new_categories(self, local_product_categories_list):

        for categorie in self.OFF_categories:
            if categorie not in local_product_categories_list:
                local_categorie = self.categorie_manager.select_based_on_name(categorie)
                try:
                    local_categorie_name = local_categorie[0]['name']
                    self.product_categorie_manager.insert(local_categorie_name, self.OFF_name)
                except IndexError:
                    print('La catégorie n\'existe pas')
                    self.categorie_manager.insert(categorie)
                    self.product_categorie_manager.insert(categorie, self.OFF_name)

    def _update_store_information(self, local_product):
        local_product_stores_id, local_product_stores_list = self._make_local_product_stores_list()

        print('C - Magasin(s) enregistré(s) en local : ', local_product_stores_list)  # A supprimer
        print('D - Magasin(s) récupéré(s) sur OFF : ', self.OFF_stores)  # A supprimer

        self._remove_obsolete_stores(local_product, local_product_stores_id, local_product_stores_list)
        self._add_new_stores(local_product_stores_list)

    def _make_local_product_stores_list(self):

        local_product_stores_id = self.product_store_manager.select_based_on_product_id(self.OFF_code)

        local_product_stores_list = []

        # print('1 - local_product_stores_id.all() : ', local_product_stores_id.all())  # A supprimer
        # print('2 - len(local_product_stores_id) : ', len(local_product_stores_id.all()))  # A supprimer

        for i in range(len(local_product_stores_id.all())):
            store_name = self.store_manager.select_based_on_id(local_product_stores_id[i]['store_id'])
            local_product_stores_list.append(store_name)

        return local_product_stores_id, local_product_stores_list

    def _remove_obsolete_stores(self, local_product, local_product_stores_id, local_product_stores_list):

        for i in range(len(local_product_stores_list)):
            if local_product_stores_list[i] not in self.OFF_stores:
                self.product_store_manager.delete(self.OFF_code, local_product_stores_id[i]['store_id'])

                product_store = self.product_store_manager.select_based_on_store_id(local_product_stores_id[i]['store_id'])
                try:
                    store_id = product_store[0]['store_id']
                    print(f'Le magasin {store_id} est associé à d\'autre(s) produit(s). On le conserve.')
                except IndexError:
                    # print(f'Le magasin {store_id} n\'est associé à aucun autre produit. On la supprime')
                    print('Le magasin n\'est associé à aucun autre produit. On le supprime')
                    self.store_manager.delete(local_product_stores_list[i])

    def _add_new_stores(self, local_product_stores_list):

        for store in self.OFF_stores:
            if store not in local_product_stores_list:
                local_store = self.store_manager.select_based_on_name(store)
                try:
                    local_store_name = local_store[0]['name']
                    self.product_store_manager.insert(local_store_name, self.OFF_name)
                except IndexError:
                    print('Le magasin n\'existe pas')
                    self.store_manager.insert(store)
                    self.product_store_manager.insert(store, self.OFF_name)

    def _save_update_date(self):
        last_update_date = time()

        with open('last_update', "wb") as f:
            my_pickler = pickle.Pickler(f)
            my_pickler.dump(last_update_date)


def main():
    DatabaseUpdater()


if __name__ == '__main__':
    main()
