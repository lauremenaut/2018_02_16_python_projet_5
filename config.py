#! /usr/bin/env phyton3
# coding: utf-8

""" Contains configuration data """

from records import Database

import datetime

from params import MYSQL_ID, MYSQL_PW


# db_name = "healthier_food_" + str(datetime.datetime.now())
# Problème de droits d'accès à la base !
db_name = "healthier_food"

# database = Database(f'mysql+pymysql://{MYSQL_ID}:{MYSQL_PW}@localhost/?charset=utf8')
database = Database(f'''mysql+pymysql://{MYSQL_ID}:\
{MYSQL_PW}@localhost/{db_name}?charset=utf8''')

# Tags for nutrition_grades of healthy and unhealthy products
nutrition_grades = ["a", "b", "d", "e"]

# Tags for (unhealthy) products categories
tag_categories = ["Pizzas",
                  "Céréales pour petit-déjeuner",
                  "Snacks sucrés",
                  "Confiseries"
                  ]
                  # "Sodas",
                  # "Plats préparés",
                  # "Produits laitiers",
                  # "Produits à tartiner",
                  # "Crèmes glacées",
                  # "Fromages"

"""

Requête pour récupérer les ids des catégories qui contiennent au moins 10 produits sains :

SELECT Product_Categorie.categorie_id, COUNT(*) AS nb_products
FROM Product
JOIN Product_Categorie
ON Product_Categorie.product_id = Product.product_id
WHERE Product.nutrition_grade = "a" OR Product.nutrition_grade = "b"
GROUP BY Product_Categorie.categorie_id
HAVING nb_products > 10
ORDER BY nb_products;


Requête pour récupérer le nom de des categories correspondant à ces ids:

SELECT name
FROM Categorie
WHERE categorie_id IN (47, 48, 798, 31, 1057, 1220, 997, 24, 811, 922);
WHERE categorie_id IN (2, 44, 1007, 826, 55, 45, 49, 1014, 46, 56);

WHERE categorie_id IN ();
WHERE categorie_id IN ();

WHERE categorie_id IN (1,27, 23, 22, 26, 25, 29, 28, 31);
WHERE categorie_id IN (635, 33, 30, 633, 632, 36, 34, 1102, 38, 37);
WHERE categorie_id IN (2, 35, 1106, 591, 1104, 592, 1103, 40, 39);


SELECT Product.product_id
FROM Product
WHERE Product.name = "Ferme et fondant, chocolat noir (0,8 % mg) 4 pots";

SELECT store_id
FROM Product_Store
WHERE product_id = (SELECT Product.product_id
FROM Product
WHERE Product.name = "Ferme et fondant, chocolat noir (0,8 % mg) 4 pots");

SELECT Store.name
FROM Store
WHERE store_id = (SELECT store_id
FROM Product_Store
WHERE product_id = (SELECT Product.product_id
FROM Product
WHERE Product.name = "Ferme et fondant, chocolat noir (0,8 % mg) 4 pots"));

"""
