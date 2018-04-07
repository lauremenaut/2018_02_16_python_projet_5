#! /usr/bin/env python3
# coding: utf-8

""" Sets HistoryManager class.

HistoryManager class sets methods containing queries to interact with
History table.

"""


class HistoryManager:

    """ Sets HistoryManager class.

    Class consists of 2 methods :
        - insert()
        - select()

    """

    def __init__(self, database):
        """ HistoryManager constructor.

        Sets 'self.database' attribute.

        """
        self.database = database

    def insert(self, unhealthy_product, name, description, stores, url):
        """ Manages insertion of given information into History table.

        Adds query information (= unhealthy and healthy product
        information) into History table.

        """
        self.database.query('''INSERT INTO History
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
        """ Manages selection of information.

        Returns selected query information (= unhealthy and healthy
        product information) from History table.

        """
        last_results = self.database.query('''SELECT *
                                           FROM History
                                           ORDER BY request_date DESC
                                           LIMIT 10''')
        return last_results
