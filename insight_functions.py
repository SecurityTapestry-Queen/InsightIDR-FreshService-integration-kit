#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Module providing functions to Investigations.py"""

import os
import json
from datetime import datetime
import requests

global last_time_data
global investigations
global item
global comment_data
global ticket_id
global comment
global config

FS_API = os.getenv("FS_API")

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
    IDR_API = os.getenv(config[client]['api'])
    headers = {"X-Api-Key": IDR_API, "Accept-version": "investigations-preview"}
    params = {
        "statuses": "OPEN,INVESTIGATING",
        "multi-customer": True,
        "sources": "ALERT,USER",
        "priorities": "CRITICAL,HIGH,MEDIUM,LOW",
    }
    r = requests.get(url, headers=headers, params=params)
    global investigations
    investigations = r.json()["data"]

def check_for_new(client):
    """Use lasttime to determine if new investigations are posted"""
    print("Anything New?")
    for i in investigations:
        created = datetime.strptime(i["created_time"], "%Y-%m-%dT%H:%M:%S.%fZ")
        checktime = datetime.strptime(last_time_data, "%Y-%m-%dT%H:%M:%S.%fZ")
        if checktime > created:
            continue
        global item
        item = i
        post_ticket_to_fs(client)
        get_investigation_comments(item["rrn"],client)

def update_last_time(client):
    """Update time per client in config.json"""
    with open('config.json', 'w', encoding='UTF-8') as config_file:
        config[client]["time"] = str(datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        json.dump(config, config_file, indent=4)

def post_ticket_to_fs(client):
    """Posting ticket to FreshService"""
    url = "https://securitytapestry.freshservice.com/api/v2/tickets"

    e = config[client]["email"]
    if "ccs" in config[client]:
        ccs = config[client]["ccs"]
    else: ccs = []

    if item["priority"] == "LOW":
        idr_priority = 1
        idr_urgency = 1
        idr_impact = 1
    elif item["priority"] == "MEDIUM":
        idr_priority = 2
        idr_urgency = 2
        idr_impact = 2
    elif item["priority"] == "HIGH":
        idr_priority = 3
        idr_urgency = 3
        idr_impact = 3
    elif item["priority"] == "CRITICAL":
        idr_priority = 4
        idr_urgency = 3
        idr_impact = 3

    data = {
        "description": item["title"],
        "subject": "Security Investigation: " + item["title"],
        "email": e,
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
    r = requests.post(
        url,
        auth=(FS_API, "X"),
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
    )
    ticket_id = r.json()["ticket"]["id"]
    print("Posted ticket #" + str(ticket_id))

def get_investigation_comments(t_id,client):
    """Fetch Comments from InsightIDR"""
    url = "https://us2.api.insight.rapid7.com/idr/v1/comments"
    IDR_API = os.getenv(config[client]['api'])
    headers = {"X-Api-Key": IDR_API, "Accept-version": "comments-preview"}
    params = {"multi-customer": True, "target": t_id}

    r = requests.get(url, headers=headers, params=params)
    global comment_data
    comments = r.json()
    comment_data = comments["data"]
    global comment
    for comment in comment_data:
        created = datetime.strptime(comment["created_time"], "%Y-%m-%dT%H:%M:%S.%fZ")
        checktime = datetime.strptime(last_time_data, "%Y-%m-%dT%H:%M:%S.%fZ")

        if checktime > created:
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
