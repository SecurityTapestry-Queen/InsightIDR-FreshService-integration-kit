#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import json
import os
from datetime import datetime

global lasttimedata
global investigations
global item
global commentdata
global ticketID
global comment
global config

FS_API = os.getenv("FS_API")

def whenWasTheLastTime(client):
    with open('config.json', 'r') as configfile:
        global config
        config = json.load(configfile)
    global lasttimedata
    lasttimedata = config[client]["time"]


def getInsightInvestigations(client):
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

def checkForNew(client):
    print("Anything New?")
    for i in investigations:
        created = datetime.strptime(i["created_time"], "%Y-%m-%dT%H:%M:%S.%fZ")
        checktime = datetime.strptime(lasttimedata, "%Y-%m-%dT%H:%M:%S.%fZ")
        if checktime > created:
            continue
        else:
            global item
            item = i
            postTicketToFS(client)
            getInvestigationComments(item["rrn"],client)

def updateLastTime(client):
    with open('config.json', 'w') as configfile:
        config[client]["time"] = str(datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        json.dump(config, configfile, indent=4)

def postTicketToFS(client):
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
    global ticketID
    r = requests.post(
        url,
        auth=(FS_API, "X"),
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
    )
    ticketID = r.json()["ticket"]["id"]
    print("Posted ticket #" + str(ticketID))

def getInvestigationComments(id,client):
    url = "https://us2.api.insight.rapid7.com/idr/v1/comments"
    IDR_API = os.getenv(config[client]['api'])
    headers = {"X-Api-Key": IDR_API, "Accept-version": "comments-preview"}
    params = {"multi-customer": True, "target": id}

    r = requests.get(url, headers=headers, params=params)
    global commentdata
    comments = r.json()
    commentdata = comments["data"]
    global comment
    for comment in commentdata:
        created = datetime.strptime(comment["created_time"], "%Y-%m-%dT%H:%M:%S.%fZ")
        checktime = datetime.strptime(lasttimedata, "%Y-%m-%dT%H:%M:%S.%fZ")

        if checktime > created:
            continue
        elif comment["body"] is None:
            continue
        else:
            postCommentsToFS(str(ticketID))

def postCommentsToFS(fsID):
    webhook_url = (
        "https://securitytapestry.freshservice.com/api/v2/tickets/" + fsID + "/notes"
    )
    data = {"body": comment["body"], "private": False}
    requests.post(
        webhook_url,
        auth=(FS_API, "X"),
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
    )
    print("Posted comment to ticket #" + str(fsID))

def Investigations(client):
    whenWasTheLastTime(client)
    getInsightInvestigations(client)
    checkForNew(client)
    updateLastTime(client)