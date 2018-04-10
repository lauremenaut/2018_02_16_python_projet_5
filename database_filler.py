#! /usr/bin/env python3
# coding: utf-8

""" Sets DatabaseFiller class.

DatabaseFiller class fills local MySQL database retrieving data from
Open Food Facts API.

"""

from requests import get

from category_manager import CategoryManager
from config import database_connection, nutrition_grades, tag_categories
from product_category_manager import ProductCategoryManager
from product_manager import ProductManager
from product_store_manager import ProductStoreManager
from store_manager import StoreManager


class DatabaseFiller:

    """ Sets DatabaseFiller class.

    Consists of 3 private methods :
        - __init__()
        - _get_products()
        - _fill_db()

    """

    def __init__(self, database):
        """ DatabaseFiller constructor.

        For each category and for each nutrition grade, retrieves
        corresponding products from Open Food Facts API and adds them to
        local database.

        """
        # self.database = database
        # Creates instances of table manager classes
        self.product_manager = ProductManager(database)
        self.category_manager = CategoryManager(database)
        self.product_category_manager = ProductCategoryManager(database)
        self.store_manager = StoreManager(database)
        self.product_store_manager = ProductStoreManager(database)

        for nutrition_grade in nutrition_grades:
            for category in tag_categories:
                products = self._get_products(category, nutrition_grade)
                self._fill_db(products)

    def _get_products(self, category, nutrition_grade):
        """ Return a list of dictionnaries of products information.

        Connects to Open Food Facts API via get() method from requests
        library and sends requests using given criteria for categories
        and nutrition grades.
        json content from response object contains products information.

        """
        criteria = {
            'action': 'process',
            'json': 1,
            'countries': 'France',
            'page_size': 100,
            'page': 1,
            'tagtype_0': 'categories',
            'tag_contains_0': 'contains',
            'tag_0': category,
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

    def _fill_db(self, products):
        """ Manages database filling.

        Checks for each product whether required data is available or
        not.
        If so, product is added to local database.

        """
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
                for category in categories_to_strip:
                    self.categories.append(category.strip().capitalize())
                stores_to_strip = (product['stores']).split(',')
                self.stores = []
                for store in stores_to_strip:
                    self.stores.append(store.strip().capitalize())
                self.nutrition_grade = product['nutrition_grades'].lower()

            except KeyError:
                print('Missing data', file=open('print_log.txt', 'a'))

            if all([self.code, self.name, self.description, self.brand,
                    self.url, self.nutrition_grade, self.categories[0],
                    self.stores[0]]):
                self.product_manager.insert(self.code, self.name,
                                            self.description, self.brand,
                                            self.url, self.nutrition_grade)
                for category in self.categories:
                    self.category_manager.insert(category)
                    self.product_category_manager.insert(category, self.name)
                for store in self.stores:
                    self.store_manager.insert(store)
                    self.product_store_manager.insert(store, self.name)


def main():
    database = database_connection()
    DatabaseFiller(database)

if __name__ == '__main__':
    main()
