#! /usr/bin/env phyton3
# coding: utf-8

""" Sets App class.

App class manages interactions with the user.

"""

import argparse

from db_creator import DB_Creator
from db_updater import DB_Updater
from config import database, tag_categories


class App:
    """ Sets App class.

    Consists of 6 methods :
        - __init__()
        - choose_categorie()
        - choose_unhealthy_product()
        - get_healthy_product()
        - save_result()
        - get_saved_result()

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
            DB_Creator()
            DB_Updater()
        # database.query('USE healthier_food')
        carry_on = True

        while carry_on:
            print("\nQue souhaitez-vous faire ?")
            print('''\n1 - Chercher une alternative plus saine à un nouvel \
aliment''')
            print("2 - Retrouver vos substitutions enregistrées")
            print("3 - Quitter l'application")

            try:
                starting_choice = int(input("\n"))
                assert starting_choice in [1, 2, 3]
            except ValueError:
                print("\nVeuillez saisir un nombre : 1, 2 ou 3.")
                continue
            except AssertionError:
                print("\n{} est un choix invalide. Veuillez saisir 1, 2 ou 3."
                      .format(starting_choice))
                continue
            else:
                if starting_choice == 1:
                    categorie = self.choose_categorie()
                    unhealthy_product = \
                        self.choose_unhealthy_product(categorie)
                    healthy_product = \
                        self.get_healthy_product(unhealthy_product, categorie)
                    self.save_result(unhealthy_product, healthy_product)
                elif starting_choice == 2:
                    self.get_saved_results()
                elif starting_choice == 3:
                    print("\nMerci de votre visite !\n")
                    carry_on = False

    def choose_categorie(self):
        """ Displays a list of indexed categories and returns the chosen
        one. """
        print("\nVeuillez saisir le numéro de la categorie de votre choix :\n")
        for categorie in tag_categories:
            position = tag_categories.index(categorie) + 1
            print(f"{position} - {categorie}")

        try:
            categorie_choice = int(input("\n"))
        except ValueError:
            print("Saisie invalide")
            self.choose_categorie()
        except IndexError:
            print("Saisie invalide")
            self.choose_categorie()

        selected_categorie = tag_categories[categorie_choice - 1]
        return selected_categorie  # Est-ce mieux de mettre des 'return' ou des 'self' ??

    def choose_unhealthy_product(self, categorie):
        """ Retrieves unhealthy products from chosen categorie in local
        database, displays 10 of them and returns the chosen one. """
        unhealthy_products = \
            database.query('''SELECT Product.name
                           FROM Product
                           JOIN Product_Categorie
                           ON Product.product_id = Product_Categorie.product_id
                           JOIN Categorie
                           ON Categorie.categorie_id = \
                               Product_Categorie.categorie_id
                           WHERE Categorie.name = :selected_categorie
                           AND (Product.nutriscore = "e" OR \
                               Product.nutriscore = "d")''',
                           selected_categorie=categorie)

        print(f"\nVeuillez maintenant saisir le numéro d'un produit de la \
categorie {categorie} :\n")

        # Comment accéder au nombre de produits ? L'objet "unhealthy_products"
        # n'a pas de longueur ...

        for i in range(10):
            try:
                print(f'''{i + 1} - \
{unhealthy_products[i]['name'].capitalize()}''')
            except IndexError:
                pass

        try:
            unhealthy_product_choice = int(input("\n"))
        except ValueError:
            print("Saisie invalide")
            self.choose_unhealthy_product()
        except IndexError:
            print("Saisie invalide")
            self.choose_unhealthy_product()

        selected_unhealthy_product = \
            unhealthy_products[unhealthy_product_choice - 1]["name"]
        return selected_unhealthy_product

    def get_healthy_product(self, unhealthy_product, categorie):
        """ Returns the best matching healthy product and its
        information """

        # Retrieves id of categories to which belongs the chosen
        # unhealthy product
        unhealthy_product_categories_id = \
            database.query('''SELECT Product_Categorie.categorie_id
                           FROM Product_Categorie
                           JOIN Product
                           ON Product.product_id = Product_Categorie.product_id
                           WHERE Product.name = :name''',
                           name=unhealthy_product)

        #  Je convertis l'objet en liste en attendant de trouver comment accéder à sa longueur ...
        unhealthy_product_categories_id_list = []

        try:
            for i in range(10):
                unhealthy_product_categories_id_list. \
                    append(unhealthy_product_categories_id[i]["categorie_id"])
        except IndexError:
            pass

        print("\n\n\n******************************************************")  # A supprimer
        print(f'''\nListe des id des categories pour \
{unhealthy_product} : {unhealthy_product_categories_id_list}\n''')  # A supprimer

        # Retrieves products from chosen categorie which nutriscore is
        # "a" or "b"
        healthy_products = \
            database.query('''SELECT Product.product_id,
                                     Product.name,
                                     Product.description,
                                     Product.url
                           FROM Product
                           JOIN Product_Categorie
                           ON Product.product_id = Product_Categorie.product_id
                           JOIN Categorie
                           ON Categorie.categorie_id = \
                               Product_Categorie.categorie_id
                           WHERE (Product.nutriscore = "a" OR \
                               Product.nutriscore = "b")
                           AND Categorie.name = :categorie''',
                           categorie=categorie)

        # Dictionnary {name of healthy product : number of categories it
        # shares with chosen unhealthy_product}
        healthy_products_dict = {}

        try:
            for i in range(20):
                # For each healthy product, retrieves categories ids
                healthy_product_categories_ids = \
                    database.query('''SELECT Product_Categorie.categorie_id
                                   FROM Product_Categorie
                                   JOIN Product
                                   ON Product.product_id = \
                                       Product_Categorie.product_id
                                   WHERE Product.name = :name''',
                                   name=healthy_products[i]["name"])

                # For each healthy product, makes a list of categories
                # it shares with chosen unhealthy product
                shared_categories = []
                try:
                    for j in range(10):
                        if healthy_product_categories_ids[j]["categorie_id"] \
                                in unhealthy_product_categories_id_list:
                            shared_categories. \
                                append(healthy_product_categories_ids[j]
                                       ["categorie_id"])
                except IndexError:
                    pass

                healthy_products_dict[healthy_products[i]["name"]] = \
                    len(shared_categories)

                print(f'''id des categories en commun avec {unhealthy_product}\
 pour {healthy_products[i]['name']} : {shared_categories}''')  # A supprimer

        except IndexError:
            pass

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

        print(f"\nNombre maximum de catégories en commun = {maximum}")  # A supprimer
        print(f'''\nProduits sains qui partagent {maximum} catégories avec\
 {unhealthy_product} : ''')  # A supprimer
        for match in best_matches:
            print(f'- {match}')
        print("\n******************************************************\n\n\n")  # A supprimer

        # List of best matching healthy products which nutriscore is "a"
        healthiest_matches = []

        for match in best_matches:
            healthy_match = database.query('''SELECT name, nutriscore
                                           FROM Product
                                           WHERE name = :name
                                           AND nutriscore = "a"''',
                                           name=match)
            try:
                healthiest_matches.append(healthy_match[0]["name"])
            except IndexError:
                pass

        # 'healthiest_match' comes from "a" products list
        # ('healthiest_matches') if not empty, else from "b" (and "a")
        # products list ('best_matches')
        try:
            healthiest_match = healthiest_matches[0]
        except IndexError:
            healthiest_match = best_matches[0]

        # Retrieves information for the product proposed to the user
        # ('healthiest_match')
        proposed_product = \
            database.query('''SELECT Product.product_id,
                                     Product.name,
                                     Product.description,
                                     Product.url
                           FROM Product
                           WHERE Product.name = :name''',
                           name=healthiest_match)

        # Retrieves id of stores selling the proposed product
        store_ids = database.query('''SELECT Product_Store.store_id
                                   FROM Product_Store
                                   JOIN Product
                                   ON Product.product_id = \
                                       Product_Store.product_id
                                   WHERE Product.name = :name''',
                                   name=healthiest_match)

        # List of stores selling the proposed product
        self.stores = []

        try:  # Pas terrible ce try/except ... comment faire mieux ??
            for i in range(10):
                store = database.query('''SELECT Store.name
                                       FROM Store
                                       WHERE Store.store_id = :store_id''',
                                       store_id=store_ids[i]["store_id"])
                self.stores.append(store[0]["name"])
        except IndexError:
            pass

            self.stores_str = ', '.join(self.stores)

        print(f"\nVoici une alternative plus saine à '{unhealthy_product}' :")
        print(f"\nNom : {(proposed_product[0]['name'])}")
        print(f"Description : {proposed_product[0]['description']}")
        print(f"Disponible chez : {self.stores_str}")

        print(f"{proposed_product[0]['url']}")

        return proposed_product

    def save_result(self, unhealthy_product, healthy_product):
        """ Allows the user to save the result of its query """
        print("\nSouhaitez-vous enregistrer ce résultat pour le retrouver plus\
 tard ?\n")
        print("1 - Oui, je sauvegarde")
        print("2 - Non, merci")

        try:
            backup_choice = int(input("\n"))
            assert backup_choice in [1, 2]
        except ValueError:
            print("\nVeuillez saisir un nombre : 1 ou 2.")
            self.save_result()
        except AssertionError:
            print(f'''\n{backup_choice} est un choix invalide. Veuillez \
saisir 1 ou 2.''')
            self.save_result()
        else:
            # Relevant information is added in History table
            if backup_choice == 1:
                database.query('''INSERT INTO History
                               VALUES (NULL,
                                       NOW(),
                                       :unhealthy_product,
                                       :healthy_product,
                                       :description,
                                       :stores,
                                       :url)''',
                               unhealthy_product=unhealthy_product,
                               healthy_product=healthy_product[0]["name"],
                               description=healthy_product[0]["description"],
                               stores=self.stores_str,
                               url=healthy_product[0]["url"])

                print("\nRésultat sauvegardé !")
            elif backup_choice == 2:
                pass

    def get_saved_results(self):
        """ Allows the user to retrieve old queries """
        saved_results = database.query("""SELECT *
                                       FROM History
                                       ORDER BY request_date DESC
                                       LIMIT 5""")

        print("\nVoici les résultats de vos dernières recherches :")

        for saved_result in saved_results:
            print(f"\nDate de la recherche : {saved_result['request_date']}")
            print(f"Produit substitué : {saved_result['unhealthy_product']}")
            print(f"Produit proposé : {saved_result['healthy_product']}")
            print(f"Description : {saved_result['description']}")
            print(f"Disponible chez : {saved_result['stores']}")
            print(f"{saved_result['url']}")


def parse_arguments():
    """ Returns an arguments parser with an "update" argument. """
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--update", action="store_true",
                        help="database update")
    return parser.parse_args()


def main():
    argument = parse_arguments()
    App(argument.update)


if __name__ == "__main__":
    main()
