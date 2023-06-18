#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Module providing functions to Investigations.py"""

import os
import sys
import json
from datetime import datetime
import requests # pylint: disable=E0401

last_time_data = None
investigations = None
investigation_item = None
comment_data = None
ticket_id = None
comment = None
config = None

fs_api = os.getenv("FS_API")


def function_check():
    """Functional Check for Python 3.10+ and fs_api secret"""
    print('Performing Function Check')
    if sys.version_info < (3, 10):
        sys.exit('Python 3.10+ Needed')
    if str(fs_api) == 'None':
        sys.exit('FS_API key missing')
    print('Function Check Succeeded')

def when_was_the_last_time(client):
    """Check lasttime checked from config.json"""
    with open('config.json', 'r', encoding='UTF-8') as config_file:
        global config
        config = json.load(config_file)
    global last_time_data
    last_time_data = config[client]["time"]

def get_insight_investigations(client):
    """Fetch Investigations from InsightIDR"""
    print("Getting Open Investigations for "+ str(client))
    url = "https://us2.api.insight.rapid7.com/idr/v2/investigations"
    idr_api = os.getenv(config[client]['api'])
    headers = {"X-Api-Key": idr_api, "Accept-version": "investigations-preview"}
    params = {
        "statuses": "OPEN,INVESTIGATING",
        "multi-customer": True,
        "sources": "ALERT,USER",
        "priorities": "CRITICAL,HIGH,MEDIUM,LOW",
    }
    request = requests.get(url, headers=headers, params=params)
    global investigations
    investigations = request.json()["data"]

def check_for_new(client):
    """Use lasttime to determine if new investigations are posted"""
    print("Anything New?")
    for investigation in investigations:
        created_time = datetime.strptime(investigation["created_time"], "%Y-%m-%dT%H:%M:%S.%fZ")
        checked_time = datetime.strptime(last_time_data, "%Y-%m-%dT%H:%M:%S.%fZ")
        if checked_time > created_time:
            continue
        global investigation_item
        investigation_item = investigation
        post_ticket_to_fs(client)
        get_investigation_comments(investigation_item["rrn"],client)

def update_last_time(client):
    """Update time per client in config.json"""
    with open('config.json', 'w', encoding='UTF-8') as config_file:
        config[client]["time"] = str(datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        json.dump(config, config_file, indent=4)

def post_ticket_to_fs(client):
    """Posting ticket to FreshService"""
    url = "https://securitytapestry.freshservice.com/api/v2/tickets"

    email = config[client]["email"]
    if "ccs" in config[client]:
        ccs = config[client]["ccs"]
    else: ccs = []

    if investigation_item["priority"] == "LOW":
        idr_priority = 1
        idr_urgency = 1
        idr_impact = 1
    elif investigation_item["priority"] == "MEDIUM":
        idr_priority = 2
        idr_urgency = 2
        idr_impact = 2
    elif investigation_item["priority"] == "HIGH":
        idr_priority = 3
        idr_urgency = 3
        idr_impact = 3
    elif investigation_item["priority"] == "CRITICAL":
        idr_priority = 4
        idr_urgency = 3
        idr_impact = 3

    data = {
        "description": investigation_item["title"],
        "subject": "Security Investigation: " + investigation_item["title"],
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
    global ticket_id
    request = requests.post(
        url,
        auth=(fs_api, "X"),
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
    )
    ticket_id = request.json()["ticket"]["id"]
    print("Posted ticket #" + str(ticket_id))

def get_investigation_comments(t_id,client):
    """Fetch Comments from InsightIDR"""
    url = "https://us2.api.insight.rapid7.com/idr/v1/comments"
    idr_api = os.getenv(config[client]['api'])
    headers = {"X-Api-Key": idr_api, "Accept-version": "comments-preview"}
    params = {"multi-customer": True, "target": t_id}

    request = requests.get(url, headers=headers, params=params)
    global comment_data
    comments = request.json()
    comment_data = comments["data"]
    global comment
    for comment in comment_data:
        created_time = datetime.strptime(comment["created_time"], "%Y-%m-%dT%H:%M:%S.%fZ")
        checked_time = datetime.strptime(last_time_data, "%Y-%m-%dT%H:%M:%S.%fZ")

        if checked_time > created_time:
            continue
        if comment["body"] is None:
            continue
        post_comments_to_fs(str(ticket_id))

def post_comments_to_fs(fs_id):
    """Posting comments from InsightIDR to FreshService"""
    webhook_url = (
        "https://securitytapestry.freshservice.com/api/v2/tickets/" + fs_id + "/notes"
    )
    data = {"body": comment["body"], "private": False}
    requests.post(
        webhook_url,
        auth=(fs_api, "X"),
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
