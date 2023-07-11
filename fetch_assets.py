#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Module performing Bot Activity - Assets Search"""

from insight_functions import *  # pylint: disable=W0401,W0614

if __name__ == "__main__":
    function_check()
    config = fetch_config()
    clients = []
    for key in config["Clients"]:
        clients.append(key)
    for client in clients:
        if config["Clients"][client]["enabled"] is True:
            fetch_assets_by_rrn(client)
        else:
            print(str(client) + " is Disabled.")