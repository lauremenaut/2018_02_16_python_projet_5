#! /usr/bin/env python3
# coding: utf-8

""" Sets DatabaseUpdater class.

DatabaseUpdater class manages information updating for each product of
local MySQL database one-by-one.

"""

from time import time

from requests import get

from category_manager import CategoryManager
from config import database_connection
from product_category_manager import ProductCategoryManager
from product_manager import ProductManager
from product_store_manager import ProductStoreManager
from store_manager import StoreManager


class DatabaseUpdater:

    """ Sets DatabaseUpdater class.

    Consists of 14 private methods :
        - __init__()
        - _run()
        - _get_products_codes()
        - _get_OFF_product()
        - _update_new_information()
        - _update_categories_information()
        - _get_local_product_categories_information()
        - _remove_obsolete_categories()
        - _add_new_categories()
        - _update_stores_information()
        - _get_local_product_stores_information()
        - _remove_obsolete_stores()
        - _add_new_stores()
        - _save_update_date()

    """

    def __init__(self, database):
        """ DatabaseUpdater constructor.

        Creates instances of table manager classes.
        Runs _run() method.

        """
        self.product_manager = ProductManager(database)
        self.category_manager = CategoryManager(database)
        self.product_category_manager = ProductCategoryManager(database)
        self.store_manager = StoreManager(database)
        self.product_store_manager = ProductStoreManager(database)

        self._run(database)

    def _run(self, database):
        """ Manages database update.

        For each product of local database, checks information &
        updates if necessary.
        Saves update date.

        """
        codes = self._get_products_codes(database)

        for i in range(len(codes.all())):
            try:
                self._get_OFF_product(codes, i)
                local_product = self.product_manager.\
                    select_product_information(self.OFF_code)
                self._update_new_information(local_product)
                self._update_categories_information(local_product)
                self._update_stores_information(local_product)
            except KeyError as e:
                print('Aïe, KeyError : ', e, file=open('print_log.txt', 'a'))

        self._save_update_date()

    def _get_products_codes(self, database):
        """ Manages product codes retrieving.

        Returns 'codes' object containing product id for all products of
        the local database.

        """
        codes = database.query('''SELECT Product.product_id FROM Product''')
        return codes

    def _get_OFF_product(self, codes, i):
        """ Manages product information retrieving.

        For a given product code, collects product information from Open
        Food Facts API using get() method from request library.

        """
        response = get(f'''https://fr.openfoodfacts.org/api/v0/product/\
{codes[i]['product_id']}.json''')
        data = response.json()
        OFF_product = data['product']

        self.OFF_code = OFF_product['code']
        self.OFF_name = OFF_product['product_name'].strip().capitalize()
        self.OFF_description = OFF_product['generic_name'].capitalize()
        OFF_brands = (OFF_product['brands']).split(',')
        self.OFF_brand = OFF_brands[0].capitalize()
        OFF_categories_to_strip = (OFF_product['categories']).split(',')
        self.OFF_categories = []
        for category in OFF_categories_to_strip:
            self.OFF_categories.append(category.strip().capitalize())
        OFF_stores_to_strip = (OFF_product['stores']).split(',')
        self.OFF_stores = []
        for store in OFF_stores_to_strip:
            self.OFF_stores.append(store.strip().capitalize())
        self.OFF_nutrition_grade = OFF_product['nutrition_grades'].lower()

    def _update_new_information(self, local_product):
        """ Manages information updating, except categories and stores.

        Compares product information from local database vs. from Open
        Food Facts API.
        Updates information when needed.

        """
        if local_product[0]['name'] != self.OFF_name:
            self.product_manager.update_name(self.OFF_name, self.OFF_code)
            print('"name" updated !', file=open('print_log.txt', 'a'))
        if local_product[0]['description'] != self.OFF_description:
            self.product_manager.update_description(
                self.OFF_description, self.OFF_code)
            print('"description" updated !', file=open('print_log.txt', 'a'))
        if local_product[0]['brand'] != self.OFF_brand:
            self.product_manager.update_brand(self.OFF_brand, self.OFF_code)
            print('"brand" updated !', file=open('print_log.txt', 'a'))
        if local_product[0]['nutrition_grade'] != self.OFF_nutrition_grade:
            self.product_manager.update_nutrition_grade(
                self.OFF_nutrition_grade, self.OFF_code)
            print('"nutrition_grade" updated !', file=open('print_log.txt', 'a'))

    def _update_categories_information(self, local_product):
        """ Manages categories information updating.

        - Retrieves categories information for local product.
        - Removes obsolete categories from local database.
        - Adds new categories from Open Food Facts into local database.

        """
        local_product_categories_id, local_product_categories_list = \
            self._get_local_product_categories_information()

        self._remove_obsolete_categories(local_product,
                                         local_product_categories_id,
                                         local_product_categories_list)
        self._add_new_categories(local_product_categories_list)

    def _get_local_product_categories_information(self):
        """ Manages retrieving of categories information.

        Returns categories id object & list of categories name for local
        product.

        """
        local_product_categories_id = self.product_category_manager.\
            select_based_on_product_id(self.OFF_code)

        local_product_categories_list = []

        for i in range(len(local_product_categories_id.all())):
            category_name = self.category_manager.select_based_on_id(
                local_product_categories_id[i]['category_id'])
            local_product_categories_list.append(category_name)

        return local_product_categories_id, local_product_categories_list

    def _remove_obsolete_categories(self, local_product,
                                    local_product_categories_id,
                                    local_product_categories_list):
        """ Manages obsolete categories removing.

        Removes categories from local database which don't appear
        anymore in Open Food Facts platform.

        """
        for i in range(len(local_product_categories_list)):
            if local_product_categories_list[i] not in self.OFF_categories:
                self.product_category_manager.delete(
                    self.OFF_code,
                    local_product_categories_id[i]['category_id'])

                product_category = self.product_category_manager.\
                    select_based_on_category_id(
                        local_product_categories_id[i]['category_id'])
                try:
                    category_id = product_category[0]['category_id']
                    # with open('print_log.txt', 'a') as f:
                    print(f'La catégorie {category_id} est associée à \
d\'autre(s) produit(s). On la conserve.', file=open('print_log.txt', 'a'))
                except IndexError:
                    # with open('print_log.txt', 'a') as f:
                    print('La catégorie n\'est associée à aucun autre \
produit. On la supprime', file=open('print_log.txt', 'a'))
                    self.category_manager.delete(
                        local_product_categories_list[i])

    def _add_new_categories(self, local_product_categories_list):
        """ Manages new categories addition.

        Adds new categories from Open Food Facts platform into local
        database.

        """
        for category in self.OFF_categories:
            if category not in local_product_categories_list:
                local_category = self.category_manager.\
                    select_based_on_name(category)
                try:
                    local_category_name = local_category[0]['name']
                    self.product_category_manager.insert(
                        local_category_name, self.OFF_name)
                except IndexError:
                    print('La catégorie n\'existe pas', file=open('print_log.txt', 'a'))
                    self.category_manager.insert(category)
                    self.product_category_manager.insert(
                        category, self.OFF_name)

    def _update_stores_information(self, local_product):
        """ Manages stores information updating.

        - Retrieves stores information for local product.
        - Removes obsolete stores from local database.
        - Adds new stores from Open Food Facts into local database.

        """
        local_product_stores_id, local_product_stores_list = \
            self._get_local_product_stores_information()

        self._remove_obsolete_stores(local_product, local_product_stores_id,
                                     local_product_stores_list)
        self._add_new_stores(local_product_stores_list)

    def _get_local_product_stores_information(self):
        """ Manages retrieving of stores information.

        Returns stores id object & list of stores name for local
        product.

        """
        local_product_stores_id = self.product_store_manager.\
            select_based_on_product_id(self.OFF_code)

        local_product_stores_list = []

        for i in range(len(local_product_stores_id.all())):
            store_name = self.store_manager.select_based_on_id(
                local_product_stores_id[i]['store_id'])
            local_product_stores_list.append(store_name)

        return local_product_stores_id, local_product_stores_list

    def _remove_obsolete_stores(self, local_product, local_product_stores_id,
                                local_product_stores_list):
        """ Manages obsolete stores removing.

        Removes stores from local database which don't appear
        anymore in Open Food Facts platform.

        """
        for i in range(len(local_product_stores_list)):
            if local_product_stores_list[i] not in self.OFF_stores:
                self.product_store_manager.delete(
                    self.OFF_code, local_product_stores_id[i]['store_id'])

                product_store = self.product_store_manager.\
                    select_based_on_store_id(
                        local_product_stores_id[i]['store_id'])
                try:
                    store_id = product_store[0]['store_id']
                    print(f'Le magasin {store_id} est associé à \
d\'autre(s) produit(s). On le conserve.', file=open('print_log.txt', 'a'))
                except IndexError:
                    print('Le magasin n\'est associé à aucun autre \
produit. On le supprime', file=open('print_log.txt', 'a'))
                    self.store_manager.delete(local_product_stores_list[i])

    def _add_new_stores(self, local_product_stores_list):
        """ Manages new stores addition.

        Adds new stores from Open Food Facts platform into local
        database.

        """
        for store in self.OFF_stores:
            if store not in local_product_stores_list:
                local_store = self.store_manager.select_based_on_name(store)
                try:
                    local_store_name = local_store[0]['name']
                    self.product_store_manager.insert(local_store_name,
                                                      self.OFF_name)
                except IndexError:
                    print('Le magasin n\'existe pas', file=open('print_log.txt', 'a'))
                    self.store_manager.insert(store)
                    self.product_store_manager.insert(store, self.OFF_name)

    def _save_update_date(self):
        """ Manages saving of database update date.

        Saves the date into an external 'last_update.txt' file.

        """
        update_date = str(time())

        with open('last_update.txt', "w") as f:
            f.write(update_date)


def main():
    database = database_connection()
    DatabaseUpdater(database)


if __name__ == '__main__':
    main()
