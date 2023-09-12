#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Module to fetch all investigation data from freshservice"""

import json
import requests

USER_KEY = "" # Remove when done testing locally

ticket_list = []

def ticket_request():
    url = "https://securitytapestry.freshservice.com/api/v2/tickets"
    pages = 9
    user_key = USER_KEY
    headers = (user_key, "X")

    for page in range(pages):
        page += 1
        params = {
            "include": "stats",
            "updated_since": "2022-08-01",
            "order_type": "asc",
            "per_page": "100",
            "page": page
        }

        try:
            request = requests.get( url, params, auth=headers, timeout=30 ).json()["tickets"]
        except KeyError:
            print(f"Issue obtaining data from page {page}")

        ticket_list.extend(request)

    ticket_dump = json.dumps(ticket_list, indent=4)
    with open("ticket_list.json","w",encoding="UTF-8") as outfile:
        outfile.write(ticket_dump)

if __name__ == "__main__":
    ticket_request()
