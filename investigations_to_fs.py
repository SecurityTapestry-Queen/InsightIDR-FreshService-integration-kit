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

    function_check()

    for c in clients:

        with open('config.json', 'r', encoding='UTF-8') as config_file:

            config = json.load(config_file)

            if config[c]['enabled'] is True:
                investigation_post(c)
            else:

                print (str(c) + ' is Disabled.')
