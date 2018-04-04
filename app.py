#! /usr/bin/env python3
# coding: utf-8

""" Sets UpdateThread & App classes.

UpdateThread class sets a thread allowing to launch database update
while user runs the application.

App class manages the application running : interactions with the user,
healthy product choice, launching creation or update of local database
if required.

"""

from threading import Thread
from os import path
from time import time
from argparse import ArgumentParser

from config import tag_categories
from database_creator import DatabaseCreator
from tables_creator import TablesCreator
from database_filler import DatabaseFiller
from database_updater import DatabaseUpdater
from product_manager import ProductManager
from product_categorie_manager import ProductCategorieManager
from store_manager import StoreManager
from product_store_manager import ProductStoreManager
from history_manager import HistoryManager


class UpdateThread(Thread):
    """ Sets UpdateThread class.

    Consists of 2 methods :
        - __init__()
        - run()

    """
    def __init__(self):
        """ UpdateThread constructor."""
        Thread.__init__(self)

    def run(self):
        """
        Sets 'is_updating' variable (useful for proper use of .join())
        Calls DatabaseUpdater()

        """
        self.is_updating = True
        DatabaseUpdater()


class App:
    """ Sets App class.

    Consists of 12 methods :
        - __init__()
        - _display_menu()
        - _choose_categorie()
        - _choose_unhealthy_product()
        - _get_unhealthy_product_categories_id()
        - _get_healthy_products()
        - _get_best_matches()
        - _get_healthiest_match()
        - _get_stores()
        - _display_result()
        - _save_result()
        - _get_saved_results()

    """
    def __init__(self, db_create, db_update):
        """ App constructor.

        Creates local database if specified by user with 'db_create'
        parsed argument.
        Updates local database if specified by user with 'db_update'
        parsed argument.
        Checks if last local database update is older than 7 days, and
        launch update if needed.
        Creates instances of needed 'Table Manager' classes
        Runs the interaction with the user

        """
        # database.query('USE healthier_food')

        if db_create:
            DatabaseCreator()
            TablesCreator()
            DatabaseFiller()

        if db_update:
            DatabaseUpdater()

        update_thread = UpdateThread()
        update_thread.is_updating = False
        delta_jour = self._get_delay_since_last_update()
        if delta_jour > 7:
            update_thread.start()

        # Creates instances of table manager classes
        self.product_manager = ProductManager()
        self.product_categorie_manager = ProductCategorieManager()
        self.store_manager = StoreManager()
        self.product_store_manager = ProductStoreManager()
        self.history_manager = HistoryManager()

        self._run()

        if update_thread.is_updating:
            update_thread.join()

    def _get_delay_since_last_update(self):
        """ Retrieves last update date, calculates and returns the delay
        until now (number of days)

        """
        if path.exists('last_update.txt'):
            with open('last_update.txt', "r") as f:
                last_update_date = float(f.read())

            delta_secondes = time() - last_update_date
            delta_jour = delta_secondes / (60*60*24)

            print('Nombre de secondes écoulées depuis la dernière mise à jour : ', delta_secondes)  # A supprimer
            print('Nombre de jours écoulés depuis la dernière mise à jour : ', delta_jour)  # A supprimer

        else:
            delta_jour = 0

        return delta_jour

    def _run(self):
        """ Manages app running.


        """
        carry_on = True

        while carry_on:
            self._display_menu()
            try:
                starting_choice = int(input('\n'))
                assert starting_choice in [1, 2, 3]
            except ValueError:
                print('\nVeuillez saisir un nombre : 1, 2 ou 3.')
                continue
            except AssertionError:
                print(f'''\n{starting_choice} est un choix invalide. Veuillez \
saisir 1, 2 ou 3.''')
                continue
            else:
                if starting_choice == 1:
                    categorie = self._choose_categorie()
                    unhealthy_product = \
                        self._choose_unhealthy_product(categorie)
                    categories_id = \
                        self._get_unhealthy_product_categories_id(
                            unhealthy_product)
                    healthy_products = \
                        self._get_healthy_products(categorie, categories_id)
                    best_matches = \
                        self._get_best_matches(healthy_products)
                    proposed_product = \
                        self._get_healthiest_match(best_matches)
                    stores = self._get_stores(proposed_product)
                    self._display_result(unhealthy_product, proposed_product,
                                         stores)
                    self._save_result(unhealthy_product, proposed_product,
                                      stores)
                elif starting_choice == 2:
                    self._get_saved_results()
                elif starting_choice == 3:
                    print('\nMerci de votre visite !\n')
                    carry_on = False

    def _display_menu(self):
        """ Displays 3 choices for the user :

        - Looking for a new substitution and save it
        - Retrieving old substitutions
        - Quit

        """
        print('\nQue souhaitez-vous faire ?')
        print('''\n1 - Chercher une alternative plus saine à un nouvel \
aliment''')
        print('2 - Retrouver vos substitutions enregistrées')
        print('3 - Quitter l\'application')

    def _choose_categorie(self):
        """ Displays a list of indexed categories and returns the one
        chosen by user.

        """
        carry_on = True

        while carry_on:
            print('\nVeuillez saisir le numéro correspondant à la categorie de \
votre choix :\n')
            for categorie in tag_categories:
                position = tag_categories.index(categorie) + 1
                print(f'{position} - {categorie}')

            try:
                categorie_choice = int(input('\n'))
                assert categorie_choice in range(1, len(tag_categories) + 1)
                carry_on = False
            except ValueError:
                print('Saisie invalide.')
                continue
            except AssertionError:
                print(f'\n{categorie_choice} est un choix invalide.')
                continue

        selected_categorie = tag_categories[categorie_choice - 1]
        return selected_categorie

    def _choose_unhealthy_product(self, categorie):
        """ Displays 10 unhealthy products of chosen categorie from local
        database and returns the one chosen by user.

        """
        unhealthy_products = self.product_manager.select_products_information(
            categorie, 'd', 'e')

        carry_on = True

        while carry_on:
            print(f'''\nVeuillez saisir le numéro d'un produit de la categorie \
{categorie} :\n''')

            for i in range(len(unhealthy_products.all())):
                print(f'{i + 1} - \
{unhealthy_products[i]["name"].capitalize()}')

            try:
                unhealthy_product_choice = int(input('\n'))
                assert unhealthy_product_choice in range(
                    1, len(unhealthy_products.all()) + 1)
                carry_on = False
            except ValueError:
                print('Saisie invalide')
                continue
            except AssertionError:
                print(f'\n{unhealthy_product_choice} est un choix invalide.')
                continue

        selected_unhealthy_product = unhealthy_products[
            unhealthy_product_choice - 1]["name"].capitalize()
        return selected_unhealthy_product

    def _get_unhealthy_product_categories_id(self, unhealthy_product):
        """ Returns a list of categories id to which belongs the chosen
        unhealthy product

        """
        unhealthy_product_categories_id = self.product_categorie_manager.\
            select_based_on_product_name(unhealthy_product)

        unhealthy_product_categories_id_list = []
        for i in range(len(unhealthy_product_categories_id.all())):
            unhealthy_product_categories_id_list.append(
                unhealthy_product_categories_id[i]['categorie_id'])

        return unhealthy_product_categories_id_list

    def _get_healthy_products(self, categorie,
                              unhealthy_product_categories_id_list):
        """ Returns a dictionnary of healthy products (= products of the
        chosen categorie which nutrition grade is 'a' or 'b') :
          - key is name of healthy product
          - value is number of categories this healthy product shares
        with chosen unhealthy product

        """
        healthy_products = self.product_manager.select_products_information(
            categorie, 'a', 'b')

        healthy_products_dict = {}

        for i in range(len(healthy_products.all())):
            # For each healthy product, retrieves categories ids
            healthy_product_categories_id = self.product_categorie_manager.\
                select_based_on_product_name(healthy_products[i]['name'])

            # For each healthy product, makes a list of categories
            # it shares with chosen unhealthy product
            shared_categories = []
            try:  # Pourquoi ça ne fonctionne pas si j'enlève le Try/Except ?? A supprimer
                for j in range(len(healthy_products.all())):
                    if healthy_product_categories_id[j]['categorie_id'] \
                            in unhealthy_product_categories_id_list:
                        shared_categories. \
                            append(healthy_product_categories_id[j]
                                   ['categorie_id'])
            except IndexError:
                pass

            # Fills the dict with {product name : number of shared categories}
            healthy_products_dict[healthy_products[i]['name']] = \
                len(shared_categories)

        return healthy_products_dict

    def _get_best_matches(self, healthy_products_dict):
        """ Returns a list of names of products that share the maximum
        number of categories with the chosen unhealthy product

        """
        # Gets the maximum number of categories that an healthy product
        # shares with the chosen unhealthy product
        maximum = max(healthy_products_dict.values())

        # List of healthy products which share the maximum number of
        # categories with the chosen unhealthy product
        best_matches = []

        for name, number_of_shared_categories in healthy_products_dict.items():
            if number_of_shared_categories == maximum:
                best_matches.append(name)

        return best_matches

    def _get_healthiest_match(self, best_matches):
        """ Returns a product object that shares the maximum number of
        categories with the chosen unhealthy product and whose nutrition
        grade is as high as possible

        """
        # List of best matching healthy products which nutrition grade is 'a'
        healthiest_matches = []

        for match in best_matches:
            healthy_match = self.product_manager.select_match_information(
                match)

            try:
                healthiest_matches.append(healthy_match[0]['name'])
            except IndexError:
                pass

        # 'healthiest_match' comes from 'a' products list
        # ('healthiest_matches') if not empty, else from 'b'
        # products list ('best_matches')
        try:
            healthiest_match = healthiest_matches[0]
        except IndexError:
            healthiest_match = best_matches[0]

        # Retrieves information for the product proposed to the user
        # (= 'healthiest_match')
        proposed_product = self.product_manager.\
            select_healthiest_match_information(healthiest_match)

        return proposed_product

    def _get_stores(self, proposed_product):
        """ Returns a string of joined store names which sell the
        proposed product

        """
        # Retrieves id of stores selling the proposed product
        stores_id = self.product_store_manager.select_based_on_product_name(
            proposed_product[0]['name'])

        # List of stores selling the proposed product
        stores = []

        for i in range(len(stores_id.all())):
            store = self.store_manager.select_based_on_id(
                stores_id[i]['store_id'])
            stores.append(store)

        stores_str = ', '.join(stores)

        return stores_str

    def _display_result(self, unhealthy_product, proposed_product, stores_str):
        """ Displays the proposed product and its information to the user

        """
        print(f'\nVoici une alternative plus saine à "{unhealthy_product}" :')
        print(f'\nNom : {(proposed_product[0]["name"])}')
        print(f'Description : {proposed_product[0]["description"]}')
        print(f'Disponible chez : {stores_str}')

        print(f'{proposed_product[0]["url"]}')

        return proposed_product

    def _save_result(self, unhealthy_product, proposed_product, stores_str):
        """ Allows the user to save the result of its query """
        print('\nSouhaitez-vous enregistrer ce résultat pour le retrouver plus\
 tard ?\n')
        print('1 - Oui, je sauvegarde')
        print('2 - Non, merci')

        carry_on = True

        while carry_on:
            try:
                backup_choice = int(input('\n'))
                assert backup_choice in [1, 2]
            except ValueError:
                print('\nVeuillez saisir un nombre : 1 ou 2.')
                continue
            except AssertionError:
                print(f'''\n{backup_choice} est un choix invalide. Veuillez \
saisir 1 ou 2.''')
                continue
            else:
                # Relevant information is added in History table
                if backup_choice == 1:
                    self.history_manager.insert(unhealthy_product,
                                                proposed_product[0]['name'],
                                                proposed_product[0]
                                                ['description'],
                                                stores_str,
                                                proposed_product[0]['url'])

                    print('\nRésultat sauvegardé !')
                elif backup_choice == 2:
                    pass
                carry_on = False

    def _get_saved_results(self):
        """ Displays 10 last saved results """
        saved_results = self.history_manager.select()

        print('\nVoici les résultats de vos dernières recherches :')

        for saved_result in saved_results:
            print(f'\nDate de la recherche : {saved_result["request_date"]}')
            print(f'Produit substitué : {saved_result["unhealthy_product"]}')
            print(f'Produit proposé : {saved_result["healthy_product"]}')
            print(f'Description : {saved_result["description"]}')
            print(f'Disponible chez : {saved_result["stores"]}')
            print(f'{saved_result["url"]}')


def parse_arguments():
    """ Returns an argument parser with 'db_create' & 'db_update'
    arguments.

    """
    parser = ArgumentParser()
    parser.add_argument('-c', '--db_create', action='store_true',
                        help='database creation')
    parser.add_argument('-u', '--db_update', action='store_true',
                        help='database update')
    return parser.parse_args()


def main():
    argument = parse_arguments()
    App(argument.db_create, argument.db_update)


if __name__ == '__main__':
    main()
