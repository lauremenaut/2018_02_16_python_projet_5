#! /usr/bin/env phyton3
# coding: utf-8

""" Sets Update_thread class.

App class manages ...

"""

from threading import Thread

import os
import pickle
import time

from database_updater import DatabaseUpdater
from app import App


class AppThread(Thread):
    """ Sets App_thread class.

    Consists of 2 methods :

    """
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        App(update=False)


class UpdateThread(Thread):
    """ Sets Update_thread class.

    Consists of 2 methods :

    """
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        DatabaseUpdater()


# Création des threads
app_thread = AppThread()
update_thread = UpdateThread()

# Lancement des threads
app_thread.start()

if os.path.exists('last_update'):
    with open('last_update', "rb") as f:
        my_depickler = pickle.Unpickler(f)
        last_update_date = my_depickler.load()

    delta_secondes = time.time() - last_update_date

    delta_jour = delta_secondes / (60*60*24)

    print('Nombre de secondes écoulées depuis la dernière mise à jour : ', delta_secondes)
    print('Nombre de jours écoulés depuis la dernière mise à jour : ', delta_jour)

    if delta_jour > 7:
        update_thread.start()

# # Attend que les threads se terminent, faut-il le laisser ???
app_thread.join()
# update_thread.join()
