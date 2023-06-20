#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Module performing Bot Activity"""

from insight_functions import *  # pylint: disable=W0401,W0614

if __name__ == "__main__":
    function_check()
    last_checked_tickets_to_close = fetch_config()["Other"]["last_checked_tickets_to_close"]
    new_time = str(datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"))