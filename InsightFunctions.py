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
global times

FS_API = os.getenv("FS_API")

def whenWasTheLastTime(client):
    with open('times.json', 'r') as timefile:
        global times
        times = json.load(timefile)
    global lasttimedata
    lasttimedata = times[client]


def getInsightInvestigations(client):
    print("Getting Open Investigations for "+ str(client))
    url = "https://us2.api.insight.rapid7.com/idr/v2/investigations"
    if client == "Lab": IDR_API = os.getenv("IDR_API_L4")
    if client == "LOM": IDR_API = os.getenv("IDR_API_LEXUS")
    if client == "HSSD": IDR_API = os.getenv("IDR_API_HSSD")
    if client == "MHC": IDR_API = os.getenv("IDR_API_MHC")
    if client == "ICS": IDR_API = os.getenv("IDR_API_ICS")
    if client == "GosM": IDR_API = os.getenv("IDR_API_GOSSETT")
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
    with open('times.json', 'w') as timefile:
        times[client] = str(datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
        json.dump(times, timefile)

def postTicketToFS(client):
    url = "https://securitytapestry.freshservice.com/api/v2/tickets"

    with open('emails.json', 'r') as emailfile:
        emails = json.load(emailfile)
        e = emails[client]["email"]
        if "ccs" in emails[client]:
            ccs = emails[client]["ccs"]
        else: ccs = []

    idr_priority = 1
    idr_urgency = 1
    idr_impact = 1
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
    if client == "Lab": IDR_API = os.getenv("IDR_API_L4")
    if client == "LOM": IDR_API = os.getenv("IDR_API_LEXUS")
    if client == "HSSD": IDR_API = os.getenv("IDR_API_HSSD")
    if client == "MHC": IDR_API = os.getenv("IDR_API_MHC")
    if client == "ICS": IDR_API = os.getenv("IDR_API_ICS")
    if client == "GosM": IDR_API = os.getenv("IDR_API_GOSSETT")
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
