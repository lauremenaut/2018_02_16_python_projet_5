#! /usr/bin/env python3
# coding: utf-8

""" Sets DatabaseFiller class.

DatabaseFiller class fills 'healthier_food' database, connecting with Open
Food Facts API.

"""

from requests import get

import sys

from config import database, db_name, nutrition_grades, tag_categories
from product_manager import ProductManager
from categorie_manager import CategorieManager
from product_categorie_manager import ProductCategorieManager
from store_manager import StoreManager
from product_store_manager import ProductStoreManager


# Où met-on ces 2 lignes ??
# errors_log_db_filler = open('errors_log_db_filler.txt', 'w')  # .txt non tracké (??)
# sys.stderr = errors_log_db_filler


class DatabaseFiller:  # 'Old-style class defined' ??
    """ Sets DatabaseFiller class.

    Consists of 3 private methods :
        - __init__()
        - _get_products()
        - _fill_db()

    """
    def __init__(self):
        """ DatabaseFiller constructor.

        For each categorie and for each nutrition grade, retrieves
        corresponding products from Open Food Facts API and adds them to
        local database.

        """
        for nutrition_grade in nutrition_grades:
            for categorie in tag_categories:
                products = self._get_products(categorie, nutrition_grade)
                self._fill_db(products)

    def _get_products(self, categorie, nutrition_grade):  # 'Method could be a function (no-self-used)' ??
        """ Gets products from Open Food Facts API following given
        criteria. """
        criteria = {
            'action': 'process',
            'json': 1,
            'countries': 'France',
            'page_size': 100,
            'page': 1,
            'tagtype_0': 'categories',
            'tag_contains_0': 'contains',
            'tag_0': categorie,
            'tagtype_1': 'nutrition_grades',
            'tag_contains_1': 'contains',
            'tag_1': nutrition_grade
            }

        response = get('https://fr.openfoodfacts.org/cgi/search.pl',
                       params=criteria)
        data = response.json()

        # 'products' is a list of dictionnaries
        products = data['products']
        return products

    def _fill_db(self, products):  # 'Method could be a function (no-self-used)' ??
        """ Contains SQL requests to fill database """
        # database.query('SET NAMES "utf8"')
        # database.query(f'USE {db_name}')

        # For each product, checks if required data is available or not
        for product in products:
            try:
                self.code = product['code']
                self.name = product['product_name'].strip().capitalize()
                self.description = product['generic_name'].capitalize()
                brands = (product['brands']).split(',')
                self.brand = brands[0].capitalize()
                self.url = product['url']
                categories_to_strip = (product['categories']).split(',')
                self.categories = []
                for categorie in categories_to_strip:
                    self.categories.append(categorie.strip().capitalize())
                stores_to_strip = (product['stores']).split(',')
                self.stores = []
                for store in stores_to_strip:
                    self.stores.append(store.strip().capitalize())
                self.nutrition_grade = product['nutrition_grades'].lower()

            except KeyError:
                print('Missing data')

            # If required data is available, product is added to local
            # database
            if all([self.code, self.name, self.description, self.brand, self.url,
                    self.nutrition_grade, self.categories[0], self.stores[0]]):
                ProductManager.insert(self, self.code, self.name, self.description, self.brand, self.url, self.nutrition_grade)
                for categorie in self.categories:
                    CategorieManager.insert(self, categorie)
                    ProductCategorieManager.insert(self, categorie, self.name)
                for store in self.stores:
                    StoreManager.insert(self, store)
                    ProductStoreManager.insert(self, store, self.name)

def main():
    DatabaseFiller()


if __name__ == '__main__':
    main()
