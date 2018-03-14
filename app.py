#! /usr/bin/env phyton3
# coding: utf-8

""" Sets App class.

App class manages interactions with the user.

"""

import argparse

import db_creator # Est-ce mieux d'importer seulement la classe ?
import db_updater
from config import database, categories


class App:
    """ Sets App class """
    def __init__(self, update):
        """ App constructor """

        if update:
            db_creator.DB_Creator()
            db_updater.DB_Updater()
        carry_on = True
        print("\nBonjour, que souhaitez-vous faire ?")

        while carry_on:
            print("\n1 - Chercher une alternative plus saine à un nouvel aliment")
            print("2 - Retrouver vos substitutions enregistrées")
            print("3 - Quitter l'application")

            try:
                starting_choice = int(input())
                assert starting_choice in [1, 2, 3]
            except ValueError:
                print("\nVeuillez saisir un nombre : 1, 2 ou 3.")
                continue
            except AssertionError:
                print("\n{} est un choix invalide. Veuillez saisir 1, 2 ou 3.".format(starting_choice))
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
        for categorie in categories:
            position = categories.index(categorie) + 1
            print("{} - {}".format(position, categorie))

        try:
            categorie_choice = int(input())
            self.selected_categorie = categories[categorie_choice - 1]
        except ValueError:
            print("Saisie invalide")
            self.choose_categorie()
        except IndexError:
            print("Saisie invalide")
            self.choose_categorie()

    def choose_unhealthy_product(self):
        """ Manages product selection """
        unhealthy_products = database.query("""SELECT Product.name
            FROM Product
            JOIN Product_Categorie
            ON Product.product_id = Product_Categorie.product_id
            JOIN Categorie
            ON Categorie.categorie_id = Product_Categorie.categorie_id
            WHERE Categorie.name = :selected_categorie
            AND (Product.nutriscore = "e" OR Product.nutriscore = "d")
            """, selected_categorie=self.selected_categorie)

        print("\nVeuillez maintenant saisir le numéro d'un produit de la categorie {} :\n".format(self.selected_categorie))

        # Comment accéder au nombre de produits ? L'objet "unhealthy_products" n'a pas de longueur ...

        for i in range(10):
            try:
                print("{} - {}".format(i + 1, unhealthy_products[i]["name"].capitalize()))
                i += 1
            except IndexError:
                pass

        try:
            unhealthy_product_choice = int(input())
            self.selected_unhealthy_product = unhealthy_products[unhealthy_product_choice - 1]["name"]
        except ValueError:
            print("Saisie invalide")
            self.choose_unhealthy_product()
        except IndexError:
            print("Saisie invalide")
            self.choose_unhealthy_product()

    def get_healthy_product(self):
        """ Returns an healthy product and its details """
        #  Work in progress : ajouter la correspondance de plusieurs catégories pour améliorer la pertinence du résultat
        self.healthy_products = database.query("""SELECT Product.product_id, Product.name, Product.description, Product.store_id, Product.url
            FROM Product
            JOIN Product_Categorie
            ON Product.product_id = Product_Categorie.product_id
            JOIN Categorie
            ON Categorie.categorie_id = Product_Categorie.categorie_id
            WHERE (Product.nutriscore = "a" OR Product.nutriscore = "b")
            AND Categorie.name = :selected_categorie
            """, selected_categorie=self.selected_categorie)

        for i in range(2):  # A supprimer
            print(self.healthy_products[i]["product_id"])  # A supprimer

        print("\nVoici une alternative plus saine à '{}' :\n".format(self.selected_unhealthy_product))
        print("{}".format(self.healthy_products[0]["name"]).capitalize())
        print("{}".format(self.healthy_products[0]["description"]).capitalize())
        print("Disponible chez {}".format(self.healthy_products[0]["store_id"]).capitalize())  # Remplacer l'id par le nom du magasin
        print("{}".format(self.healthy_products[0]["url"]))
        # Ajoute-t-on d'autres informations ?

    def save_result(self):
        """ Manages result backup """
        print("\nSouhaitez-vous enregistrer ce résultat pour le retrouver plus tard ?\n")
        print("1 - Oui, je sauvegarde")
        print("2 - Non, merci")

        try:
            backup_choice = int(input())
            assert backup_choice in [1, 2]
        except ValueError:
            print("\nVeuillez saisir un nombre : 1 ou 2.")
            self.save_result()
        except AssertionError:
            print("\n{} est un choix invalide. Veuillez saisir 1 ou 2.".format(backup_choice))
            self.save_result()
        else:
            if backup_choice == 1:
                database.query("""INSERT INTO History
                    VALUES (NULL, NOW(), :unhealthy_product, :healthy_product, :description, :store, :url)""",
                               unhealthy_product=self.selected_unhealthy_product,
                               healthy_product=self.healthy_products[0]["name"],
                               description=self.healthy_products[0]["description"],
                               store=self.healthy_products[0]["store_id"],
                               url=self.healthy_products[0]["url"])
                print("\nRésultat sauvegardé !")
            elif backup_choice == 2:
                pass

        print("\nQue souhaitez-vous faire maintenant ?")
        # Attention : autant de print que d'exceptions levées ...

    def get_saved_results(self):
        """ Manages """
        saved_results = database.query("""SELECT *
            FROM History
            ORDER BY request_date DESC
            LIMIT 20""")

        print("\nVoici les résultats de vos dernières recherches :")

        for saved_result in saved_results:
            print("\n{}".format(saved_result["request_date"]))
            print("Produit à substituer : '{}'".format(saved_result["unhealthy_product"]))
            print("Produit proposé : '{}'".format(saved_result["healthy_product"]))
            print("{}".format(saved_result["description"]))
            print("Disponible chez {}".format(saved_result["store"]))
            print("{}".format(saved_result["url"]))


def parse_arguments():
    """ Returns an arguments parser with an "update" argument. """
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--update", action="store_true",
                        help="database update")
    return parser.parse_args()


def main():
    argument = parse_arguments()
    app = App(argument.update)


if __name__ == "__main__":
    main()


"""
        healthy_product = self.database.query('''SELECT Product.name
            FROM (SELECT Product.name
            FROM Product
            JOIN Product_Categorie
            ON Product.product_id = Product_Categorie.product_id
            JOIN Categorie
            ON Categorie.categorie_id = Product_Categorie.categorie_id
            WHERE (Product.nutriscore = "a" OR Product.nutriscore = "b")
            AND Categorie.name = :selected_categorie)
            WHERE
            ''')

"""
