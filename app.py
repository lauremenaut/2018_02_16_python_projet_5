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
    """ Sets App class """
    def __init__(self, update):
        """ App constructor """
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
                    self.choose_categorie()
                    self.choose_unhealthy_product()
                    self.get_healthy_product()
                    self.save_result()
                elif starting_choice == 2:
                    self.get_saved_results()
                elif starting_choice == 3:
                    print("\nMerci de votre visite !\n")
                    carry_on = False

    def choose_categorie(self):
        """ Manages categorie selection """
        print("\nVeuillez saisir le numéro d'une categorie :\n")
        for categorie in tag_categories:
            position = tag_categories.index(categorie) + 1
            print(f"{position} - {categorie}")

        try:
            categorie_choice = int(input("\n"))
            self.selected_categorie = tag_categories[categorie_choice - 1]
        except ValueError:
            print("Saisie invalide")
            self.choose_categorie()
        except IndexError:
            print("Saisie invalide")
            self.choose_categorie()

    def choose_unhealthy_product(self):
        """ Manages product selection """
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
                           selected_categorie=self.selected_categorie)

        print(f"\nVeuillez maintenant saisir le numéro d'un produit de la \
categorie {self.selected_categorie} :\n")

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
            self.selected_unhealthy_product = \
                unhealthy_products[unhealthy_product_choice - 1]["name"]
        except ValueError:
            print("Saisie invalide")
            self.choose_unhealthy_product()
        except IndexError:
            print("Saisie invalide")
            self.choose_unhealthy_product()

    def get_healthy_product(self):
        """ Returns an healthy product and its details """

        unhealthy_product_categories_ids = \
            database.query('''SELECT Product_Categorie.categorie_id
                           FROM Product_Categorie
                           JOIN Product
                           ON Product.product_id = Product_Categorie.product_id
                           WHERE Product.name = :name''',
                           name=self.selected_unhealthy_product)

        unhealthy_product_categories_ids_list = []

        try:
            for i in range(10):
                unhealthy_product_categories_ids_list. \
                    append(unhealthy_product_categories_ids[i]["categorie_id"])
        except IndexError:
            pass

        print(f'''\n\n\nListe des categories_ids pour \
{self.selected_unhealthy_product} : {unhealthy_product_categories_ids_list}\n''')  # A supprimer

        self.healthy_products = \
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
                           AND Categorie.name = :selected_categorie''',
                           selected_categorie=self.selected_categorie)

        healthy_products_dict = {}

        try:
            for i in range(10):
                healthy_product_categories_ids = \
                    database.query('''SELECT Product_Categorie.categorie_id
                                   FROM Product_Categorie
                                   JOIN Product
                                   ON Product.product_id = \
                                       Product_Categorie.product_id
                                   WHERE Product.name = :name''',
                                   name=self.healthy_products[i]["name"])

                shared_categories = []
                try:
                    for j in range(10):
                        if healthy_product_categories_ids[j]["categorie_id"] \
                                in unhealthy_product_categories_ids_list:
                            shared_categories. \
                                append(healthy_product_categories_ids[j]
                                       ["categorie_id"])
                except IndexError:
                    pass

                healthy_products_dict[self.healthy_products[i]["name"]] = \
                    len(shared_categories)
                print(f'''Categories_ids en commun avec \
{self.selected_unhealthy_product} pour {self.healthy_products[i]['name']} : \
{shared_categories}''')  # A supprimer

        except IndexError:
            pass

        best_healthy_products = []

        maximum = max(healthy_products_dict.values())

        for name, number_of_shared_categories in healthy_products_dict.items():
            if number_of_shared_categories == maximum:
                best_healthy_products.append(name)

        print(f"\nNombre de catégories en commun maximum = {maximum}")  # A supprimer
        print(f'''\nProduits sains qui ont le maximum de catégories en commun \
: {best_healthy_products} \n\n\n''')  # A supprimer

        self.healthy_product = \
            database.query('''SELECT Product.product_id,
                                     Product.name,
                                     Product.description,
                                     Product.url
                           FROM Product
                           WHERE Product.name = :name''',
                           name=best_healthy_products[0])

        store_ids = database.query('''SELECT Product_Store.store_id
                                   FROM Product_Store
                                   JOIN Product
                                   ON Product.product_id = \
                                       Product_Store.product_id
                                   WHERE Product.name = :name''',
                                   name=self.healthy_products[0]["name"])

        self.stores = []

        try:  # Pas terrible ce try/except ... comment faire mieux ??
            for i in range(10):  # On ajoute maximum 10 magasins à la liste 'stores'
                store = database.query('''SELECT Store.name
                                       FROM Store
                                       WHERE Store.store_id = :store_id''',
                                       store_id=store_ids[i]["store_id"])
                self.stores.append(store[0]["name"])
        except IndexError:
            pass

        print(f'''\nVoici une alternative plus saine à \
'{self.selected_unhealthy_product}' :\n''')

        print(f"Nom : {(self.healthy_product[0]['name']).capitalize()}")
        # Pas de majuscules, malgré le capitalize, pourquoi ?!
        print(f'''Description : {(self.healthy_product[0]['description']).
            capitalize()}''')
        print("Disponible chez :")

        for store in self.stores:
            print((store).capitalize())
            # Comment imprimer les 3 magasins sur la même ligne ?

        print(f"{self.healthy_product[0]['url']}")

    def save_result(self):
        """ Manages result backup """
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
            if backup_choice == 1:
                database.query('''INSERT INTO History
                               VALUES (NULL,
                                       NOW(),
                                       :unhealthy_product,
                                       :healthy_product,
                                       :description,
                                       :store,
                                       :url)''',
                               unhealthy_product=self.
                               selected_unhealthy_product,
                               healthy_product=self.
                               healthy_product[0]["name"],
                               description=self.
                               healthy_product[0]["description"],
                               store=self.stores[0],
                               url=self.healthy_product[0]["url"])
                # Seulement 1 magasin enregistré pour le moment ...
                print("\nRésultat sauvegardé !")
            elif backup_choice == 2:
                pass

    def get_saved_results(self):
        """ Manages """
        saved_results = database.query("""SELECT *
                                       FROM History
                                       ORDER BY request_date
                                       LIMIT 10""")

        print("\nVoici les résultats de vos dernières recherches :")

        for saved_result in saved_results:
            print(f"\nDate de la recherche : {saved_result['request_date']}")
            print(f"Produit substitué : {saved_result['unhealthy_product']}")
            print(f"Produit proposé : {saved_result['healthy_product']}")
            print(f"Description : {saved_result['description']}")
            print(f"Disponible chez : {saved_result['store']}")
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
