#! /usr/bin/env phyton3
# coding: utf-8

""" Contains configuration data """

import records

# les identifiants devraient être dans un fichier séparé, ignoré par Git
database = records.Database('mysql+pymysql://lauredougui:mysql@localhost/healthier_food?charset=utf8')

nutrition_grades = ["a", "b", "d", "e"]

categories = ["Boissons sucrées", "Pains", "Biscuits", "Desserts", "Céréales au chocolat"]
