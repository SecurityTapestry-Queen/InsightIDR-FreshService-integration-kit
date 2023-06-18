#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Module performing Bot Activity"""

from insight_functions import *  # pylint: disable=W0401,W0614

if __name__ == "__main__":
    function_check()
    config = fetch_config()
    clients = []
    for key in config:
        clients.append(key)
    for client in clients:
        with open("config.json", "r", encoding="UTF-8") as config_file:
            config = json.load(config_file)
            if config[client]["enabled"] is True:
                investigation_post(client)
            else:
                print(str(client) + " is Disabled.")
