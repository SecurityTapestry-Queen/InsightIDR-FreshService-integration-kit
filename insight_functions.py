#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Module providing functions to Investigations.py"""

import os
import sys
import json
from datetime import datetime
import requests # pylint: disable=E0401

LAST_TIME_DATA = None
INVESTIGATIONS = None
INVESTIGATION_ITEM = None
COMMENT_DATA = None
TICKET_ID = None
COMMENT = None
CONFIG = None

FS_API = os.getenv("FS_API")


def function_check():
    """Functional Check for Python 3.10+ and FS_API secret"""
    print('Performing Function Check')
    if sys.version_info < (3, 10):
        sys.exit('Python 3.10+ Needed')
    if str(FS_API) == 'None':
        sys.exit('FS_API key missing')
    print('Function Check Succeeded')

def when_was_the_last_time(client):
    """Check lasttime checked from config.json"""
    with open('config.json', 'r', encoding='UTF-8') as config_file:
        global CONFIG # pylint: disable=W0603
        CONFIG = json.load(config_file)
    global LAST_TIME_DATA # pylint: disable=W0603
    LAST_TIME_DATA = CONFIG[client]["time"]

def get_insight_investigations(client):
    """Fetch Investigations from InsightIDR"""
    print("Getting Open Investigations for "+ str(client))
    url = "https://us2.api.insight.rapid7.com/idr/v2/investigations"
    idr_api = os.getenv(CONFIG[client]['api'])
    headers = {"X-Api-Key": idr_api, "Accept-version": "investigations-preview"}
    params = {
        "statuses": "OPEN,INVESTIGATING",
        "multi-customer": True,
        "sources": "ALERT,USER",
        "priorities": "CRITICAL,HIGH,MEDIUM,LOW",
    }
    request = requests.get(url, headers=headers, params=params)
    global INVESTIGATIONS # pylint: disable=W0603
    INVESTIGATIONS = request.json()["data"]

def check_for_new(client):
    """Use lasttime to determine if new investigations are posted"""
    print("Anything New?")
    for investigation in INVESTIGATIONS:
        created_time = datetime.strptime(investigation["created_time"], "%Y-%m-%dT%H:%M:%S.%fZ")
        checked_time = datetime.strptime(LAST_TIME_DATA, "%Y-%m-%dT%H:%M:%S.%fZ")
        if checked_time > created_time:
            continue
        global INVESTIGATION_ITEM # pylint: disable=W0603
        INVESTIGATION_ITEM = investigation
        post_ticket_to_fs(client)
        get_investigation_comments(INVESTIGATION_ITEM["rrn"],client)

def update_last_time(client):
    """Update time per client in config.json"""
    with open('config.json', 'w', encoding='UTF-8') as config_file:
        CONFIG[client]["time"] = str(datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        json.dump(CONFIG, config_file, indent=4)

def post_ticket_to_fs(client):
    """Posting ticket to FreshService"""
    url = "https://securitytapestry.freshservice.com/api/v2/tickets"

    email = CONFIG[client]["email"]
    if "ccs" in CONFIG[client]:
        ccs = CONFIG[client]["ccs"]
    else: ccs = []

    if INVESTIGATION_ITEM["priority"] == "LOW":
        idr_priority = 1
        idr_urgency = 1
        idr_impact = 1
    elif INVESTIGATION_ITEM["priority"] == "MEDIUM":
        idr_priority = 2
        idr_urgency = 2
        idr_impact = 2
    elif INVESTIGATION_ITEM["priority"] == "HIGH":
        idr_priority = 3
        idr_urgency = 3
        idr_impact = 3
    elif INVESTIGATION_ITEM["priority"] == "CRITICAL":
        idr_priority = 4
        idr_urgency = 3
        idr_impact = 3

    data = {
        "description": INVESTIGATION_ITEM["title"],
        "subject": "Security Investigation: " + INVESTIGATION_ITEM["title"],
        "email": email,
        "cc_emails": ccs,
        "status": 2,
        "priority": idr_priority,
        "urgency": idr_urgency,
        "impact": idr_impact,
        "source": 14,
        "group_id": 21000544549,
        "category": "InsightIDR",
    }
    global TICKET_ID # pylint: disable=W0603
    request = requests.post(
        url,
        auth=(FS_API, "X"),
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
    )
    TICKET_ID = request.json()["ticket"]["id"]
    print("Posted ticket #" + str(TICKET_ID))

def get_investigation_comments(t_id,client):
    """Fetch Comments from InsightIDR"""
    url = "https://us2.api.insight.rapid7.com/idr/v1/comments"
    idr_api = os.getenv(CONFIG[client]['api'])
    headers = {"X-Api-Key": idr_api, "Accept-version": "comments-preview"}
    params = {"multi-customer": True, "target": t_id}

    request = requests.get(url, headers=headers, params=params)
    global COMMENT_DATA # pylint: disable=W0603
    comments = request.json()
    COMMENT_DATA = comments["data"]
    global COMMENT # pylint: disable=W0603
    for COMMENT in COMMENT_DATA:
        created_time = datetime.strptime(COMMENT["created_time"], "%Y-%m-%dT%H:%M:%S.%fZ")
        checked_time = datetime.strptime(LAST_TIME_DATA, "%Y-%m-%dT%H:%M:%S.%fZ")

        if checked_time > created_time:
            continue
        if COMMENT["body"] is None:
            continue
        post_comments_to_fs(str(TICKET_ID))

def post_comments_to_fs(fs_id):
    """Posting comments from InsightIDR to FreshService"""
    webhook_url = (
        "https://securitytapestry.freshservice.com/api/v2/tickets/" + fs_id + "/notes"
    )
    data = {"body": COMMENT["body"], "private": False}
    requests.post(
        webhook_url,
        auth=(FS_API, "X"),
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
    )
    print("Posted comment to ticket #" + str(fs_id))

def investigation_post(client):
    """Bot Main Activity"""
    when_was_the_last_time(client)
    get_insight_investigations(client)
    check_for_new(client)
    update_last_time(client)
