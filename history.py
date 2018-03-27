#! /usr/bin/env phyton3
# coding: utf-8

""" Sets History class.

History class ...

"""

from config import database


class History:
    """ Sets History class.

    Class consists of 3 methods :
        - __init__()
        - insert()
        - select()

    """
    def __init__(self):
        """ History constructor """
        pass

    def insert(self, unhealthy_product, name, description, stores, url):
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
        last_results = database.query('''SELECT *
                                       FROM History
                                       ORDER BY request_date DESC
                                       LIMIT 10''')
        return last_results
