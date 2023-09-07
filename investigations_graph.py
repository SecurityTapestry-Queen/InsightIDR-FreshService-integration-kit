#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Module to produce Graph/s in relation to Investigations from InsightIDR for multiple clients"""

import json
from matplotlib import pyplot as plt
import requests


USER_KEY = "0aaedb2f-45d4-492c-be16-29014c13d70e"

ORG_ID = {
    "Lab": "cc6da3c6-9246-4fb1-ac99-6c4eb2626663",
    "HSSD": "4f89aed5-9a79-4877-8e38-1649250be0cf",
    "LOM": "787bed8a-7ac8-41bc-8337-5f093af0e025",
    "GosM": "b3b79d7b-1f3e-42f8-be0f-dc1ebf0d204c",
    "ICS": "593f982d-7eb4-4e39-8b14-83912443326b"
    }


def check_investigations():
    '''Checks Investigations from InsightIDR'''
    url = "https://us2.api.insight.rapid7.com/idr/v2/investigations/"
    idr_api = USER_KEY
    headers = {"X-Api-Key": idr_api, "Accept-version": "investigations-preview"}
    params = {
        "multi-customer": True,
        "size": 100, #Default 20
        "start_time": "2022-10-18T00:00:00Z" #Default Start Time 28 days prior
        }
    try:
        num_pages = requests.get(url, params, headers=headers, timeout=30).json()['metadata']['total_pages']
    except KeyError:
        print("Error obtaining Page Metadata")
    
    investigations_list = []
    
    lab_list = []
    hssd_list = []
    lom_list = []
    gosm_list = []
    ics_list = []

    unspecified_list = []
    low_list = []
    medium_list = []
    high_list = []
    critical_list = []

    for page in range(num_pages):
        params['index'] = page
        try:
            request = requests.get(url, params, headers=headers, timeout=30).json()['data']
        except KeyError:
            print("Error requesting Page "+str(page)+" Data")
        investigations_list.extend(request)
        page += 1

    for investigation in investigations_list:
        if investigation['organization_id'] == ORG_ID['Lab']:
            lab_list.append(investigation)
        if investigation['organization_id'] == ORG_ID['HSSD']:
            hssd_list.append(investigation)
        if investigation['organization_id'] == ORG_ID['LOM']:
            lom_list.append(investigation)
        if investigation['organization_id'] == ORG_ID['GosM']:
            gosm_list.append(investigation)
        if investigation['organization_id'] == ORG_ID['ICS']:
            ics_list.append(investigation)

    for investigation in investigations_list:
        if investigation['priority'] == "UNMAPPED":
            unspecified_list.append(investigation)
        if investigation['priority'] == "LOW":
            low_list.append(investigation)
        if investigation['priority'] == "MEDIUM":
            medium_list.append(investigation)
        if investigation['priority'] == "HIGH":
            high_list.append(investigation)
        if investigation['priority'] == "CRITICAL":
            critical_list.append(investigation)

    investigations_dump = json.dumps(investigations_list, indent=4)
    with open("investigations_json/investigations_list.json","w",encoding="UTF-8") as outfile:
        outfile.write(investigations_dump)

    lab_dump = json.dumps(lab_list, indent=4)
    with open("investigations_json/lab_list.json","w",encoding="UTF-8") as outfile:
        outfile.write(lab_dump)
    
    hssd_dump = json.dumps(hssd_list, indent=4)
    with open("investigations_json/hssd_list.json","w",encoding="UTF-8") as outfile:
        outfile.write(hssd_dump)

    lom_dump = json.dumps(lom_list, indent=4)
    with open("investigations_json/lom_list.json","w",encoding="UTF-8") as outfile:
        outfile.write(lom_dump)

    gosm_dump = json.dumps(gosm_list, indent=4)
    with open("investigations_json/gosm_list.json","w",encoding="UTF-8") as outfile:
        outfile.write(gosm_dump)

    ics_dump = json.dumps(ics_list, indent=4)
    with open("investigations_json/ics_list.json","w",encoding="UTF-8") as outfile:
        outfile.write(ics_dump)

    unspecified_dump = json.dumps(unspecified_list, indent=4)
    with open("investigations_json/unspecified_list.json","w",encoding="UTF-8") as outfile:
        outfile.write(unspecified_dump)

    low_dump = json.dumps(low_list, indent=4)
    with open("investigations_json/low_list.json","w",encoding="UTF-8") as outfile:
        outfile.write(low_dump)

    medium_dump = json.dumps(medium_list, indent=4)
    with open("investigations_json/medium_list.json","w",encoding="UTF-8") as outfile:
        outfile.write(medium_dump)

    high_dump = json.dumps(high_list, indent=4)
    with open("investigations_json/high_list.json","w",encoding="UTF-8") as outfile:
        outfile.write(high_dump)

    critical_dump = json.dumps(critical_list, indent=4)
    with open("investigations_json/critical_list.json","w",encoding="UTF-8") as outfile:
        outfile.write(critical_dump)


def load_investigations():
    '''Loads Investigations from Ephemeral File'''
    with open("investigations_json/investigations_list.json","r",encoding="UTF-8") as infile:
        investigations_loaded = json.load(infile)

    with open("investigations_json/lab_list.json","r",encoding="UTF-8") as infile:
        lab_loaded = json.load(infile)

    with open("investigations_json/hssd_list.json","r",encoding="UTF-8") as infile:
        hssd_loaded = json.load(infile)

    with open("investigations_json/lom_list.json","r",encoding="UTF-8") as infile:
        lom_loaded = json.load(infile)

    with open("investigations_json/gosm_list.json","r",encoding="UTF-8") as infile:
        gosm_loaded = json.load(infile)

    with open("investigations_json/ics_list.json","r",encoding="UTF-8") as infile:
        ics_loaded = json.load(infile)

    with open("investigations_json/unspecified_list.json","r",encoding="UTF-8") as infile:
        unspecified_loaded = json.load(infile)

    with open("investigations_json/low_list.json","r",encoding="UTF-8") as infile:
        low_loaded = json.load(infile)

    with open("investigations_json/medium_list.json","r",encoding="UTF-8") as infile:
        medium_loaded = json.load(infile)

    with open("investigations_json/high_list.json","r",encoding="UTF-8") as infile:
        high_loaded = json.load(infile)

    with open("investigations_json/critical_list.json","r",encoding="UTF-8") as infile:
        critical_loaded = json.load(infile)

    return (
        investigations_loaded,
        lab_loaded,hssd_loaded,lom_loaded,gosm_loaded,ics_loaded,
        unspecified_loaded,low_loaded,medium_loaded,high_loaded,critical_loaded
    )


def make_autopct(values):
    '''For displaying Percentage and Value on Pie Chart'''
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{v:d} ({p:.2f}%)'.format(p=pct,v=val)
    return my_autopct


def client_counts():
    '''Count by Client'''
    investigations, lab_i, hssd_i, lom_i, gosm_i, ics_i, unspec_i,low_i,medium_i,high_i,critical_i = load_investigations()
    lab_count = len(lab_i)
    hssd_count = len(hssd_i)
    lom_count = len(lom_i)
    gosm_count = len(gosm_i)
    ics_count = len(ics_i)

    return ( investigations, lab_i, hssd_i, lom_i, gosm_i, ics_i,
            lab_count, hssd_count, lom_count, gosm_count, ics_count )


def priority_counts():
    '''Count by Priority'''
    investigations, lab_i, hssd_i, lom_i, gosm_i, ics_i, unspec_i,low_i,medium_i,high_i,critical_i  = load_investigations()
    unspec_count = len(unspec_i)
    low_count = len(low_i)
    medium_count = len(medium_i)
    high_count = len(high_i)
    critical_count = len(critical_i)

    return ( investigations, unspec_i, low_i, medium_i, high_i, critical_i,
            unspec_count, low_count, medium_count, high_count, critical_count )


def investigations_pie_chart_all_clients():
    '''Creates Pie Chart based on incoming Data'''
    investigations, lab_i, hssd_i, lom_i, gosm_i, ics_i, lab_count, hssd_count, lom_count, gosm_count, ics_count = client_counts()
    client_labels = ["Lab","HSSD","LOM","GosM","ICS"]
    client_numbers = [lab_count,hssd_count,lom_count,gosm_count,ics_count]
    plt.figure(figsize=(10,7))
    plt.pie(client_numbers,labels=client_labels,autopct=make_autopct(client_numbers))
    plt.axis('equal')
    plt.suptitle("Investigations by Client")
    plt.title(str(len(investigations))+" Total (Since 10-18-2022)")
    plt.savefig("./docs/charts/investigations_all.png")


def investigations_bar_chart_all_priority():
    '''Creates Bar Chart based on incoming Data'''
    investigations, unspec_i, low_i, medium_i, high_i, critical_i, unspec_count, low_count, medium_count, high_count, critical_count = priority_counts()
    fig, ax = plt.subplots()
    investigation_labels = ["Unspecified","Low","Medium","High","Critical"]
    investigation_counts = [unspec_count,low_count,medium_count,high_count,critical_count]
    investigation_colors = ["seashell","yellow","gold","orange","orangered"]

    bars = ax.bar(investigation_labels, investigation_counts, color=investigation_colors)
    ax.bar_label(bars, fmt='{:,.0f}')
    plt.suptitle("Investigations by Priority")
    plt.title(str(len(investigations))+" Total (Since 10-18-2022)")
    plt.savefig("./docs/charts/investigations_priority.png")


if __name__ == "__main__":
    check_investigations()
    investigations_pie_chart_all_clients()
    investigations_bar_chart_all_priority()