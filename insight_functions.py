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
    if os.path.isfile("config.json") is False:
        sys.exit("config.json missing")
    if os.path.isfile("detection_rules.json") is False:
        sys.exit("detection_rules.json missing")
    print("Function Check Succeeded")


def fetch_config():
    """Load Config into memory"""
    with open("config.json", "r", encoding="UTF-8") as config_file:
        config = json.load(config_file)
        return config


def fetch_detection_rules():
    """Load Detection Rules into memory"""
    with open("detection_rules.json", "r", encoding="UTF-8") as detection_rules_file:
        detection_rules = json.load(detection_rules_file)
        return detection_rules


def update_detection_rules(new_rule):
    """Update detection rules in detection_rules.json"""
    print("Adding new Detection Rule: " + new_rule)
    detection_rules = fetch_detection_rules()
    detection_rules["detection_rules"][new_rule] = {
        "tactic": "Tactic seen, not recorded",
        "technique": "Technique seen, not recorded",
        "sub-technique": "Sub-Technique seen, not recorded"
    }
    with open("detection_rules.json", "w", encoding="UTF-8") as detection_rules_file:
        json.dump(detection_rules, detection_rules_file, indent=4)


def update_alert_types(new_alert_type):
    """Update detection rules in detection_rules.json"""
    print("Adding new Alert Type: " + new_alert_type)
    detection_rules = fetch_detection_rules()
    detection_rules["alert_types"][new_alert_type] = {
        "tactic": "Tactic seen, not recorded",
        "technique": "Technique seen, not recorded",
        "sub-technique": "Sub-Technique seen, not recorded"
    }
    with open("detection_rules.json", "w", encoding="UTF-8") as detection_rules_file:
        json.dump(detection_rules, detection_rules_file, indent=4)


def update_idr_investigation(client,rrn,fs_ticket):
    """Updating an InsightIDR Investigation via PATCH method"""
    config = fetch_config()
    url = "https://us2.api.insight.rapid7.com/idr/v2/investigations/" + rrn
    idr_api = os.getenv(config["Clients"][client]["api"])
    headers = {
    "X-Api-Key": idr_api,
    "Accept-version": "investigations-preview"
    }
    params = {
    "multi-customer": True
    }
    data = {
        "disposition": fs_ticket["disposition"],
        "status": fs_ticket["status"]
    }
    request = requests.patch(url,data,params,headers)
    updated = request.json()
    return updated


def when_was_the_last_time(client):
    """Check lasttime checked from CONFIG"""
    config = fetch_config()
    last_time_data = config["Clients"][client]["time"]
    return last_time_data


def get_alerts_from_idr(rrn, client):
    """Get Alerts from Investigation in InsightIDR"""
    config = fetch_config()
    url = 'https://us2.api.insight.rapid7.com/idr/v2/investigations/' + rrn + '/alerts'
    idr_api = os.getenv(config["Clients"][client]["api"])
    headers = {"X-Api-Key": idr_api, "Accept-version": "investigations-preview"}
    params = {"multi-customer": True}
    request = requests.get(url, headers=headers, params=params)
    alerts = request.json()
    return alerts


def get_insight_investigations(client):
    """Fetch Investigations from InsightIDR"""
    print("Checking Investigations from " + str(client))
    config = fetch_config()
    url = "https://us2.api.insight.rapid7.com/idr/v2/investigations"
    idr_api = os.getenv(config["Clients"][client]["api"])
    headers = {"X-Api-Key": idr_api, "Accept-version": "investigations-preview"}
    params = {
        "statuses": "OPEN,INVESTIGATING",
        "multi-customer": True,
        "sources": "ALERT,USER",
        "priorities": "CRITICAL,HIGH,MEDIUM,LOW",
    }
    request = requests.get(url, headers=headers, params=params)
    if "data" in request.json():
        investigations = request.json()["data"]
        check_for_new(client, investigations)
    else:
        print("Trouble getting data for " + client)
        print(request.json())


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
        print("New Investigation Detected")
        post_ticket_to_fs(investigation, client)


def update_last_time(client):
    """Update time per client in config.json"""
    config = fetch_config()
    config["Clients"][client]["time"] = str(datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
    with open("config.json", "w", encoding="UTF-8") as config_file:
        json.dump(config, config_file, indent=4)


def investigation_priority(priority):
    if priority == "LOW":
        idr_priority = 1
        idr_urgency = 1
        idr_impact = 1
    elif priority == "MEDIUM":
        idr_priority = 2
        idr_urgency = 2
        idr_impact = 2
    elif priority == "HIGH":
        idr_priority = 3
        idr_urgency = 3
        idr_impact = 3
    elif priority == "CRITICAL":
        idr_priority = 4
        idr_urgency = 3
        idr_impact = 3
    return idr_priority,idr_urgency,idr_impact

def post_ticket_to_fs(investigation, client):
    """Posting ticket to FreshService"""
    url = "https://securitytapestry.freshservice.com/api/v2/tickets"
    config = fetch_config()
    alerts = get_alerts_from_idr(investigation["rrn"], client)
    detection_rules = fetch_detection_rules()
    email = base64.b64decode(config["Clients"][client]["email"]).decode("UTF-8")
    ccs = []
    if "ccs" in config["Clients"][client]:
        for address in config["Clients"][client]["ccs"]:
            ccs.append(base64.b64decode(address).decode("UTF-8"))
    else:
        ccs = []

    idr_priority, idr_urgency, idr_impact = investigation_priority(investigation["priority"])

    if investigation["source"] == "ALERT":
        print("Fetching Alerts for: " + str(investigation["rrn"]))
        alert_title = alerts["data"][0]["title"]
        alert_type = alerts["data"][0]["alert_type"]
        alert_type_description = alerts["data"][0]["alert_type_description"]
        alert_source = alerts["data"][0]["alert_source"]
        if alerts["data"][0]["detection_rule_rrn"] is not None:
            rule = alerts["data"][0]["detection_rule_rrn"]["rule_rrn"]
            if rule in detection_rules["detection_rules"]:
                mitre_tactic = detection_rules["detection_rules"][rule]["tactic"]
                mitre_technique = detection_rules["detection_rules"][rule]["technique"]
                mitre_sub_technique = detection_rules["detection_rules"][rule]["sub-technique"]
            else:
                mitre_tactic = "Tactics, if applicable"
                mitre_technique = "Techniques, if applicable"
                mitre_sub_technique = "Sub-Techniques, if applicable"
                update_detection_rules(rule)
        else:
            rule = "N/A"
            if alert_type in detection_rules["alert_types"]:
                mitre_tactic = detection_rules["alert_types"][alert_type]["tactic"]
                mitre_technique = detection_rules["alert_types"][alert_type]["technique"]
                mitre_sub_technique = detection_rules["alert_types"][alert_type]["sub-technique"]
            else:
                mitre_tactic = "Tactics, if applicable"
                mitre_technique = "Techniques, if applicable"
                mitre_sub_technique = "Sub-Techniques, if applicable"
                update_alert_types(alert_type)
    else:
        alert_title = "N/A"
        alert_type = "N/A"
        alert_type_description = "Investigation created by user in InsightIDR"
        alert_source = "User-Made Investigation"
        mitre_tactic = "Tactics, if applicable"
        mitre_technique = "Techniques, if applicable"
        mitre_sub_technique = "Sub-Techniques, if applicable"
        rule = "N/A"

    data = {
        "description": alert_type_description,
        "subject": "Security Investigation: " + investigation["title"],
        "email": email,
        "cc_emails": ccs,
        "status": 2,
        "priority": idr_priority,
        "urgency": idr_urgency,
        "impact": idr_impact,
        "source": 1001,
        "group_id": 21000544549,
        "category": "InsightIDR",
        "custom_fields": {
            "rrn": investigation["rrn"],
            "evidence": "Place Alert Evidence here from InsightIDR",
            "research_links": "Place Research Links here, if applicable",
            "mitre_attampck_tactics_including_id_and_description": mitre_tactic,
            "mitre_attampck_techniques_including_id_and_description": mitre_technique,
            "mitre_attampck_subtechniques_including_id_and_description": mitre_sub_technique,
            "organization_id": investigation["organization_id"],
            "alert_title": alert_title,
            "alert_type": alert_type,
            "alert_type_description": alert_type_description,
            "alert_source": alert_source,
            "threat_status": investigation["disposition"],
            "detection_rule_rrn": rule
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
    idr_api = os.getenv(config["Clients"][client]["api"])
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
