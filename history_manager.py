#! /usr/bin/env python3
# coding: utf-8

""" Sets HistoryManager class.

HistoryManager class ...

"""

from config import database


class HistoryManager:
    """ Sets HistoryManager class.

    Class consists of 2 methods :
        - insert()
        - select()

    """
    def insert(self, unhealthy_product, name, description, stores, url):
        """ Adds query information (= unhealthy and healthy product
        information) into History table

        """
        database.query('''INSERT INTO History
                       VALUES (NULL,
                               NOW(),
                               :unhealthy_product,
                               :healthy_product,
                               :description,
                               :stores,
                               :url)''',
                       unhealthy_product=unhealthy_product,
                       healthy_product=name,
                       description=description,
                       stores=stores,
                       url=url)

    def select(self):
        """ Returns selected query information (= unhealthy and healthy
        product information) from History table

        """
        last_results = database.query('''SELECT *
                                       FROM History
                                       ORDER BY request_date DESC
                                       LIMIT 10''')
        return last_results
