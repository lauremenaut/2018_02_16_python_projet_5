#! /usr/bin/env phyton3
# coding: utf-8

""" Sets Update_thread class.

App class manages ...

"""

from threading import Thread

from database_creator import DatabaseCreator
from database_updater import DatabaseFiller
from app import App


class UpdateThread(Thread):
    """ Sets Update_thread class.

    Consists of 2 methods :

    """
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        DatabaseCreator()
        DatabaseFiller()


class AppThread(Thread):
    """ Sets App_thread class.

    Consists of 2 methods :

    """
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        App()  # Attention, App() attend 'update' en argument


# Création des threads
update_thread = UpdateThread()
app_thread = AppThread()

# Lancement des threads
update_thread.start()
app_thread.start()

# Attend que les threads se terminent
update_thread.join()
app_thread.join()
