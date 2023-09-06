#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Module to produce Graph/s in relation to Investigations from InsightIDR for multiple clients"""

from matplotlib import pyplot as plt
import numpy as np
import requests


USER_NAT = "0aaedb2f-45d4-492c-be16-29014c13d70e"

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
    idr_api = USER_NAT
    headers = {"X-Api-Key": idr_api, "Accept-version": "investigations-preview"}
    params = {
        "multi-customer": True,
        "size": 100, #Default 20
        "start_time": "2022-10-18T00:00:00Z" #Default Start Time 28 days prior
        }
    metadata = requests.get(url, params, headers=headers, timeout=30).json()['metadata']
    num_pages = metadata['total_pages']
    total_data = metadata['total_data']
    investigations_list = []
    lab_list = []
    hssd_list = []
    lom_list = []
    gosm_list = []
    ics_list = []

    for page in range(num_pages):
        params['index'] = page
        request = requests.get(url, params, headers=headers, timeout=30).json()['data']
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

    return investigations_list, total_data, lab_list, hssd_list, lom_list, gosm_list, ics_list


def make_autopct(values):
    '''For displaying Percentage and Value on Chart'''
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{v:d} ({p:.2f}%)'.format(p=pct,v=val)
    return my_autopct


def investigations_pie_chart_all():
    '''Creates Pie Chart based on incoming Data'''
    investigations, validated_count, lab_i, hssd_i, lom_i, gosm_i, ics_i = check_investigations()
    lab_count = len(lab_i)
    hssd_count = len(hssd_i)
    lom_count = len(lom_i)
    gosm_count = len(gosm_i)
    ics_count = len(ics_i)

    client_labels = ["Lab","HSSD","LOM","GosM","ICS"]
    client_numbers = [lab_count,hssd_count,lom_count,gosm_count,ics_count]
    plt.figure(figsize=(10,7))
    plt.pie(client_numbers,labels=client_labels,autopct=make_autopct(client_numbers))
    plt.axis('equal')
    plt.suptitle("Investigations by Client")
    plt.title(str(len(investigations))+" Total")
    plt.savefig("./docs/charts/investigations_all.png")
    
    return investigations, validated_count, lab_count, hssd_count, lom_count, gosm_count, ics_count


if __name__ == "__main__":
    investigations, validated_count, lab_count, hssd_count, lom_count, gosm_count, ics_count = investigations_pie_chart_all()
    print("Lab: " + str(lab_count))
    print("HSSD: " + str(hssd_count))
    print("LOM: " + str(lom_count))
    print("GosM: " + str(gosm_count))
    print("ICS: " + str(ics_count))
    print("Total (Since 10-18-2022): " + str(len(investigations)))
    if len(investigations) == validated_count:
        print('Success!')
        