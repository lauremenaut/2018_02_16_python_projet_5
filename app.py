#! /usr/bin/env phyton3
# coding: utf-8

""" Sets App class.

App class manages interactions with the user.

"""

import argparse

from config import database, tag_categories
from database_creator import DatabaseCreator
from database_filler import DatabaseFiller
from product import Product
from product_categorie import Product_Categorie
from product_store import Product_Store
from store import Store
from history import History


class App:
    """ Sets App class.

    Consists of 6 methods :
        - __init__()
        - _choose_categorie()
        - _choose_unhealthy_product()
        - _get_healthy_product()
        - _save_result()
        - _get_saved_result()

    """
    def __init__(self, update):
        """ App constructor.

        Updates local database if required ('update' argument parsed).
        Allows user to choose between :
        - Looking for a new substitution
        - Retrieving old substitutions
        - Quit

        """
        if update:
            DatabaseCreator()
            DatabaseFiller()
        # database.query('USE healthier_food')

        self._run()

    def _run(self):
        carry_on_1 = True

        while carry_on_1:
            print('\nQue souhaitez-vous faire ?')
            print('''\n1 - Chercher une alternative plus saine à un nouvel \
aliment''')
            print('2 - Retrouver vos substitutions enregistrées')
            print('3 - Quitter l\'application')

            try:
                starting_choice = int(input('\n'))
                assert starting_choice in [1, 2, 3]
            except ValueError:
                print('\nVeuillez saisir un nombre : 1, 2 ou 3.')
                continue
            except AssertionError:
                print(f'\n{starting_choice} est un choix invalide. Veuillez saisir 1, 2 ou 3.')
                continue
            else:
                if starting_choice == 1:
                    categorie = self._choose_categorie()
                    unhealthy_product = \
                        self._choose_unhealthy_product(categorie)
                    healthy_product = \
                        self._get_healthy_product(unhealthy_product, categorie)
                    self._save_result(unhealthy_product, healthy_product)
                elif starting_choice == 2:
                    self._get_saved_results()
                elif starting_choice == 3:
                    print('\nMerci de votre visite !\n')
                    carry_on_1 = False

    def _choose_categorie(self):
        """ Displays a list of indexed categories and returns the chosen
        one. """

        carry_on_2 = True

        while carry_on_2:
            print('\nVeuillez saisir le numéro correspondant à la categorie de votre choix :\n')
            for categorie in tag_categories:
                position = tag_categories.index(categorie) + 1
                print(f'{position} - {categorie}')

            try:
                categorie_choice = int(input('\n'))
                assert categorie_choice in range(1, len(tag_categories) + 1)
                carry_on_2 = False
            except ValueError:
                print('Saisie invalide.')
                continue
            except AssertionError:
                print(f'\n{categorie_choice} est un choix invalide.')
                continue

        selected_categorie = tag_categories[categorie_choice - 1]
        return selected_categorie

    def _choose_unhealthy_product(self, categorie):
        """ Retrieves unhealthy products from chosen categorie in local
        database, displays 10 of them and returns the chosen one. """
        unhealthy_products = Product.select_products_information(self, categorie, 'd', 'e')

        carry_on_3 = True

        while carry_on_3:
            print(f'''\nVeuillez saisir le numéro d'un produit de la categorie \
{categorie} :\n''')

            for i in range(len(unhealthy_products.all())):
                print(f'{i + 1} - {unhealthy_products[i]["name"].capitalize()}')

            try:
                unhealthy_product_choice = int(input('\n'))
                assert unhealthy_product_choice in range(1, len(unhealthy_products.all()) + 1)
                carry_on_3 = False
            except ValueError:
                print('Saisie invalide')
                continue
            except AssertionError:
                print(f'\n{unhealthy_product_choice} est un choix invalide.')
                continue

        selected_unhealthy_product = \
            unhealthy_products[unhealthy_product_choice - 1]["name"].capitalize()
        return selected_unhealthy_product

    def _get_healthy_product(self, unhealthy_product, categorie):
        """ Returns the best matching healthy product and its
        information """

        # Retrieves id of categories to which belongs the chosen
        # unhealthy product
        unhealthy_product_categories_id = Product_Categorie.select_categories_id_based_on_product_name(self, unhealthy_product)

        unhealthy_product_categories_id_list = []
        for i in range(len(unhealthy_product_categories_id.all())):
            unhealthy_product_categories_id_list.append(unhealthy_product_categories_id[i]['categorie_id'])

        print('\n\n\n******************************************************')  # A supprimer
        print(f'''\nListe des id des categories pour \
{unhealthy_product} : {unhealthy_product_categories_id.all()}\n''')  # A supprimer

        # Retrieves products from chosen categorie which nutrition_grade is
        # "a" or "b"
        healthy_products = Product.select_products_information(self, categorie, 'a', 'b')

        # Dictionnary {name of healthy product : number of categories it
        # shares with chosen unhealthy_product}
        healthy_products_dict = {}

        for i in range(len(healthy_products.all())):
            # For each healthy product, retrieves categories ids
            healthy_product_categories_ids = Product_Categorie.select_categories_id_based_on_product_name(self, healthy_products[i]['name'])

            # For each healthy product, makes a list of categories
            # it shares with chosen unhealthy product
            shared_categories = []
            try:  # Pourquoi ça ne fonctionne pas si j'enlève le Try/Except ??
                for j in range(len(healthy_products.all())):
                    if healthy_product_categories_ids[j]['categorie_id'] \
                            in unhealthy_product_categories_id_list:
                        shared_categories. \
                            append(healthy_product_categories_ids[j]
                                   ['categorie_id'])
            except IndexError:
                pass

            healthy_products_dict[healthy_products[i]['name']] = \
                len(shared_categories)

            print(f'''id des categories en commun avec {unhealthy_product}\
 pour {healthy_products[i]['name']} : {shared_categories}''')  # A supprimer

        # Gets the maximum number of categories that an healthy product
        # shares with the chosen unhealthy product
        maximum = max(healthy_products_dict.values())

        # List of healthy products which share the maximum number of
        # categories with the chosen unhealthy product
        best_matches = []

        for name, number_of_shared_categories in healthy_products_dict.items():
            # Adds an healthy product to 'best_matches' list if it
            # shares the maximum number of categories with the chosen
            # unhealthy product
            if number_of_shared_categories == maximum:
                best_matches.append(name)

        print(f'\nNombre maximum de catégories en commun = {maximum}')  # A supprimer
        print(f'''\nProduits sains qui partagent {maximum} catégories avec\
 {unhealthy_product} : ''')  # A supprimer
        for match in best_matches:
            print(f'- {match}')
        print('\n******************************************************\n\n\n')  # A supprimer

        # List of best matching healthy products which nutrition_grade is 'a'
        healthiest_matches = []

        for match in best_matches:
            healthy_match = Product.select_match_information(self, match)

            try:
                healthiest_matches.append(healthy_match[0]['name'])
            except IndexError:
                pass

        # 'healthiest_match' comes from 'a' products list
        # ('healthiest_matches') if not empty, else from 'b' (and 'a')
        # products list ('best_matches')
        try:
            healthiest_match = healthiest_matches[0]
        except IndexError:
            healthiest_match = best_matches[0]

        # Retrieves information for the product proposed to the user
        # ('healthiest_match')
        proposed_product = Product.select_healthiest_match_information(self,healthiest_match)

        # Retrieves id of stores selling the proposed product
        store_ids = Product_Store.select_stores_id(self, healthiest_match)

        # List of stores selling the proposed product
        self.stores = []

        for i in range(len(store_ids.all())):
            store = Store.select(self, store_ids[i]['store_id'])
            self.stores.append(store)

        self.stores_str = ', '.join(self.stores)

        print(f'\nVoici une alternative plus saine à "{unhealthy_product}" :')
        print(f'\nNom : {(proposed_product[0]["name"])}')
        print(f'Description : {proposed_product[0]["description"]}')
        print(f'Disponible chez : {self.stores_str}')

        print(f'{proposed_product[0]["url"]}')

        return proposed_product

    def _save_result(self, unhealthy_product, healthy_product):
        """ Allows the user to save the result of its query """
        print('\nSouhaitez-vous enregistrer ce résultat pour le retrouver plus\
 tard ?\n')
        print('1 - Oui, je sauvegarde')
        print('2 - Non, merci')

        try:
            backup_choice = int(input('\n'))
            assert backup_choice in [1, 2]
        except ValueError:
            print('\nVeuillez saisir un nombre : 1 ou 2.')
            self.save_result()
        except AssertionError:
            print(f'''\n{backup_choice} est un choix invalide. Veuillez \
saisir 1 ou 2.''')
            self.save_result()
        else:
            # Relevant information is added in History table
            if backup_choice == 1:
                History.insert(self, unhealthy_product, healthy_product[0]['name'], healthy_product[0]['description'], self.stores_str, healthy_product[0]['url'])

                print('\nRésultat sauvegardé !')
            elif backup_choice == 2:
                pass

    def _get_saved_results(self):
        """ Allows the user to retrieve old queries """
        saved_results = History.select(self)

        print('\nVoici les résultats de vos dernières recherches :')

        for saved_result in saved_results:
            print(f'\nDate de la recherche : {saved_result["request_date"]}')
            print(f'Produit substitué : {saved_result["unhealthy_product"]}')
            print(f'Produit proposé : {saved_result["healthy_product"]}')
            print(f'Description : {saved_result["description"]}')
            print(f'Disponible chez : {saved_result["stores"]}')
            print(f'{saved_result["url"]}')


def parse_arguments():
    """ Returns an arguments parser with an 'update' argument. """
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--update', action='store_true',
                        help='database update')
    return parser.parse_args()


def main():
    argument = parse_arguments()
    App(argument.update)


if __name__ == '__main__':
    main()
