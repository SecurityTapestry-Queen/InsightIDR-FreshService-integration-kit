#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Module performing Bot Activity"""

from insight_functions import *

clients = [
    'Lab',
    'LOM',
    'HSSD',
    'MHC',
    'ICS',
    'GosM',
    ]

if __name__ == '__main__':

    for c in clients:

        with open('config.json', 'r') as configfile:

            config = json.load(configfile)

            if config[c]['enabled'] is True:
                investigation_post(c)
            else:

                print (str(c) + ' is Disabled.')
