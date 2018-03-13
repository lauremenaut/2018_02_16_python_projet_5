#! /usr/bin/env phyton3
# coding: utf-8

""" Sets App class.

App class manages interactions with the user """

import records

import tags


class App:
    """ Sets App class """
    def __init__(self):
        """ App constructor """
        self.choose_categorie()
        self.choose_unhealthy_product()
        self.get_healthy_product()

    def choose_categorie(self):
        print("Veuillez saisir le numéro d'une categorie : ")
        for categorie in tags.categories:
            position = tags.categories.index(categorie) + 1
            print(position, categorie)

        try:
            categorie_choice = int(input())
            self.selected_categorie = tags.categories[categorie_choice - 1]
        except ValueError:
            print("Saisie invalide")
            self.choose_categorie()
        except IndexError:
            print("Saisie invalide")
            self.choose_categorie()

    def choose_unhealthy_product(self):
        self.database = records.Database('mysql+pymysql://lauredougui:mysql@localhost/healthier_food?charset=utf8')

        unhealthy_products = self.database.query("""SELECT Product.name FROM Product
            JOIN Product_Categorie ON Product.product_id = Product_Categorie.product_id
            JOIN Categorie ON Categorie.categorie_id = Product_Categorie.categorie_id
            WHERE Categorie.name = :selected_categorie AND (Product.nutriscore = "e" OR Product.nutriscore = "d") """, selected_categorie=self.selected_categorie)

        print("Veuillez maintenant saisir le numéro d'un produit de la categorie {} :".format(self.selected_categorie))

        # Comment accéder au nombre de produits ? L'objet "products" n'a pas de longueur ...

        for i in range(10):
            try:
                print(i + 1, unhealthy_products[i]["name"])
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
        #  Work in progress
        healthy_product = self.database.query("""SELECT Product.name
            FROM Product
            WHERE (Product.nutriscore = "a" OR Product.nutriscore = "b")""")

        print("'{}' pourrait être une alternative plus saine à '{}'.".format(healthy_product[0]["name"], self.selected_unhealthy_product))


def main():
    app = App()


if __name__ == "__main__":
    main()
