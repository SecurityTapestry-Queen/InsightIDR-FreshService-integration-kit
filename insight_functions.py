#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Module providing functions to investigations_post.py"""

import os
import sys
import json
import base64
from datetime import datetime
import requests  # pylint: disable=E0401

FS_API = os.getenv("FS_API")


def function_check():
    """Functional Check for Python 3.10+ and FS_API secret"""
    print("Performing Function Check")
    if sys.version_info < (3, 10):
        sys.exit("Python 3.10+ Needed")
    if str(FS_API) == "None":
        sys.exit("FS_API key missing")
    if os.path.isfile("config.json") == False:
        sys.exit("config.json missing")
    print("Function Check Succeeded")


def fetch_config():
    """Load Config into memory"""
    with open("config.json", "r", encoding="UTF-8") as config_file:
        config = json.load(config_file)
        return config


def when_was_the_last_time(client):
    """Check lasttime checked from CONFIG"""
    config = fetch_config()
    last_time_data = config[client]["time"]
    return last_time_data

def get_alerts_from_idr(rrn, client):
    """Get Alerts from Investigation in InsightIDR"""
    print("Fetching Alerts for Investigation RRN: " + str(rrn))
    config = fetch_config()
    url = 'https://us2.api.insight.rapid7.com/idr/v2/investigations/' + rrn + '/alerts'
    idr_api = os.getenv(config[client]["api"])
    headers = {"X-Api-Key": idr_api, "Accept-version": "investigations-preview"}
    params = {"multi-customer": True}
    request = requests.get(url, headers=headers, params=params)
    alerts = request.json()
    return alerts

def get_insight_investigations(client):
    """Fetch Investigations from InsightIDR"""
    print("Getting Open Investigations for " + str(client))
    config = fetch_config()
    url = "https://us2.api.insight.rapid7.com/idr/v2/investigations"
    idr_api = os.getenv(config[client]["api"])
    headers = {"X-Api-Key": idr_api, "Accept-version": "investigations-preview"}
    params = {
        "statuses": "OPEN,INVESTIGATING",
        "multi-customer": True,
        "sources": "ALERT,USER",
        "priorities": "CRITICAL,HIGH,MEDIUM,LOW",
    }
    request = requests.get(url, headers=headers, params=params)
    investigations = request.json()["data"]
    check_for_new(client, investigations)


def check_for_new(client, investigations):
    """Use last_time_data to determine if new investigations are posted"""
    for investigation in investigations:
        last_time_data = when_was_the_last_time(client)
        created_time = datetime.strptime(
            investigation["created_time"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        checked_time = datetime.strptime(last_time_data, "%Y-%m-%dT%H:%M:%S.%fZ")
        if checked_time > created_time:
            continue
        post_ticket_to_fs(investigation, client)


def update_last_time(client):
    """Update time per client in config.json"""
    config = fetch_config()
    config[client]["time"] = str(datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
    with open("config.json", "w", encoding="UTF-8") as config_file:
        json.dump(config, config_file, indent=4)

def post_ticket_to_fs(investigation, client):
    """Posting ticket to FreshService"""
    url = "https://securitytapestry.freshservice.com/api/v2/tickets"
    config = fetch_config()
    alerts = get_alerts_from_idr(investigation["rrn"], client)
    email = base64.b64decode(config[client]["email"]).decode("UTF-8")
    if "ccs" in config[client]:
        ccs = base64.b64decode(config[client]["ccs"]).decode("UTF-8")
    else:
        ccs = []

    if investigation["priority"] == "LOW":
        idr_priority = 1
        idr_urgency = 1
        idr_impact = 1
    elif investigation["priority"] == "MEDIUM":
        idr_priority = 2
        idr_urgency = 2
        idr_impact = 2
    elif investigation["priority"] == "HIGH":
        idr_priority = 3
        idr_urgency = 3
        idr_impact = 3
    elif investigation["priority"] == "CRITICAL":
        idr_priority = 4
        idr_urgency = 3
        idr_impact = 3

    if investigation["source"] == "ALERT":
        alert_title = alerts["data"][0]["title"]
        alert_type = alerts["data"][0]["alert_type"]
        alert_type_description = alerts["data"][0]["alert_type_description"]
        alert_source = alerts["data"][0]["alert_source"]
    else:
        alert_title = "N/A"
        alert_type = "N/A"
        alert_type_description = "N/A"
        alert_source = "N/A"

    data = {
        "description": alert_type_description,
        "subject": "Security Investigation: " + investigation["title"],
        "email": email,
        "cc_emails": ccs,
        "status": 2,
        "priority": idr_priority,
        "urgency": idr_urgency,
        "impact": idr_impact,
        "source": 15,
        "group_id": 21000544549,
        "category": "InsightIDR",
        "custom_fields": {
            "rrn": investigation["rrn"],
            "evidence": "Place Alert Evidence here from InsightIDR",
            "research_links": "Place Research Links here, if applicable",
            "mitre_attampck_tactics_including_id_and_description": "Tactics, if applicable",
            "mitre_attampck_techniques_including_id_and_description": "Techniques, if applicable",
            "mitre_attampck_subtechniques_including_id_and_description": "Sub-Techniques, if applicable",
            "organization_id": investigation["organization_id"],
            "alert_title": alert_title,
            "alert_type": alert_type,
            "alert_type_description": alert_type_description,
            "alert_source": alert_source,
            "threat_status": investigation["disposition"]
        }
    }
    request = requests.post(
        url,
        auth=(FS_API, "X"),
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
    )
    ticket_id = request.json()["ticket"]["id"]
    print("Posted ticket #" + str(ticket_id))
    get_investigation_comments(investigation["rrn"], client, ticket_id)


def get_investigation_comments(t_id, client, ticket_id):
    """Fetch Comments from InsightIDR"""
    url = "https://us2.api.insight.rapid7.com/idr/v1/comments"
    config = fetch_config()
    idr_api = os.getenv(config[client]["api"])
    headers = {"X-Api-Key": idr_api, "Accept-version": "comments-preview"}
    params = {"multi-customer": True, "target": t_id}

    request = requests.get(url, headers=headers, params=params)
    comments = request.json()
    comment_data = comments["data"]
    last_time_data = when_was_the_last_time(client)
    for comment in comment_data:
        created_time = datetime.strptime(
            comment["created_time"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        checked_time = datetime.strptime(last_time_data, "%Y-%m-%dT%H:%M:%S.%fZ")

        if checked_time > created_time:
            continue
        if comment["body"] is None:
            continue
        post_comments_to_fs(str(ticket_id), comment)


def post_comments_to_fs(fs_id, comment):
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
    get_insight_investigations(client)
    update_last_time(client)
