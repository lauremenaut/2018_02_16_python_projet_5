#! /usr/bin/env phyton3
# coding: utf-8

import records
import requests

criteria = {
            "action" : "process",
            "json" : 1,
            "countries" : "France",
            "page_size" : 20,
            "page" : 6,
            "tagtype_0" : "categories",
            "tag_contains_0" : "contains",
            "tag_0" : "sodas"
            }


r = requests.get('https://world.openfoodfacts.org/cgi/search.pl', params=criteria)

data = r.json()
products = data["products"] # products est une liste de dictionnaires correspondant aux produits de la page 1

db = records.Database('mysql+pymysql://lauredougui:crampagna09@localhost/healthier_food?charset=utf8')

for product in products:
    try:
        categories = product["categories"]
        name = product["product_name"]
        description = product["generic_name"]
        brands = (product["brands"]).split(",")
        brand = brands[0]
        url = product["url"]
        stores = (product["stores"]).split(",")
        store = stores[0]
        nutrition_grade = product["nutrition_grades"]

        if categories and name and description and brand and url and store and nutrition_grade:
            db.query('INSERT IGNORE INTO Product (name, description, brand, url, nutriscore) \
                VALUES (:name, :description, :brand, :url, :nutrition_grade)', \
                name=name, description=description, brand=brand, url=url, nutrition_grade=nutrition_grade \
                )
            db.query('INSERT IGNORE INTO Store (name) VALUES (:store)', store=store)

            for categorie in categories.split(","):
                db.query('INSERT IGNORE INTO Categorie (name) VALUES (:categorie)', categorie=categorie)

            db.query('INSERT IGNORE INTO Product_Categorie (product_id) \
                SELECT product_id FROM Product WHERE name = :name', name=name)
            db.query('UPDATE Product SET store_id = \
                (SELECT store_id FROM Store WHERE name = :store) \
                WHERE name = :name', store=store, name=name)

    except KeyError:
        print("Missing data")

print(len(products))
