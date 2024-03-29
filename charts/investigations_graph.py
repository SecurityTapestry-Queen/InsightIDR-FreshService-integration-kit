#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Module to produce Graph/s in relation to Investigations from InsightIDR for multiple clients"""

import json
from collections import Counter
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import requests


USER_KEY = "" # Remove when done testing locally

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


def convert_json_to_dataframe(json_data):
    '''Convert the JSON data to a Pandas DataFrame for easier manipulation'''
    dataframe = pd.DataFrame(json_data)

    # Helper function to convert time strings to datetime objects
    def to_datetime(series):
        return pd.to_datetime(series, errors='coerce')

    # Convert time-related columns to datetime format
    time_columns = ['last_accessed', 'created_time', 'first_alert_time', 'latest_alert_time']
    for col in time_columns:
        dataframe[col] = to_datetime(dataframe[col])

    return dataframe


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
    plt.savefig("../docs/charts/investigations_all.png")


def investigations_donut_all_clients():
    '''Creates Donut Chart based on incoming data'''
    investigations, lab_i, hssd_i, lom_i, gosm_i, ics_i, lab_count, hssd_count, lom_count, gosm_count, ics_count = client_counts()
    client_labels = ["Lab","HSSD","LOM","GosM","ICS"]
    client_numbers = [lab_count,hssd_count,lom_count,gosm_count,ics_count]
    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
    wedges, texts = ax.pie(client_numbers, wedgeprops=dict(width=0.5), startangle=-40)
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"), bbox=bbox_props, zorder=0, va="center")

    for i, p in enumerate(wedges):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = f"angle,angleA=0,angleB={ang}"
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(client_labels[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                horizontalalignment=horizontalalignment, **kw)
        
    plt.suptitle("Investigations by Client")
    ax.set_title(str(len(investigations))+" Total (Since 10-18-2022)", y=0.95)
    plt.savefig("../docs/charts/investigations_all_clients_donut.png")


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
    plt.savefig("../docs/charts/investigations_priority.png")


def investigations_time_series_creation_all():
    '''Count the number of investigations created each day, Create the time series plot'''
    with open("investigations_json/investigations_list.json","r",encoding="UTF-8") as infile:
        investigations_loaded = json.load(infile)
        dataframe = convert_json_to_dataframe(investigations_loaded)
    time_series_data = dataframe.resample('D', on='created_time').size()

    plt.figure(figsize=(14, 6))
    plt.plot(time_series_data.index,time_series_data.values,
             marker='o', linestyle='-', color='purple')
    plt.xlabel('Created Time')
    plt.ylabel('Number of Investigations')
    plt.title('Number of Investigations Created Over Time')
    plt.grid(True)
    plt.savefig("../docs/charts/investigations_time_series_creation_all.png")

def investigations_time_priority_creation_all():
    '''Count the number of investigations created each day, Create the time series plot'''
    with open("investigations_json/investigations_list.json","r",encoding="UTF-8") as infile:
        investigations_loaded = json.load(infile)
        dataframe = convert_json_to_dataframe(investigations_loaded)
    time_series_data_by_priority = dataframe.groupby('priority').resample('D', on='created_time').size().reset_index(name='count')

    # Create the line chart
    plt.figure(figsize=(14, 6))
    sns.lineplot(x='created_time', y='count', hue='priority', data=time_series_data_by_priority, markers=True, dashes=False)
    plt.xlabel('Created Time')
    plt.ylabel('Number of Investigations')
    plt.title('Number of Investigations Created Over Time by Priority')
    plt.legend(title='Priority')
    plt.grid(True)
    plt.savefig("../docs/charts/investigations_time_priority_creation_all.png")


def investigations_histogram_frequency_distribution():
    '''Creates Frequency Distribution of Investigation Creation Times'''
    with open("investigations_json/investigations_list.json","r",encoding="UTF-8") as infile:
        investigations_loaded = json.load(infile)
        dataframe = convert_json_to_dataframe(investigations_loaded)

    # Extract the hour of the day when each investigation was created
    dataframe['created_hour'] = dataframe['created_time'].dt.hour

    # Create the histogram
    plt.figure(figsize=(10, 6))
    plt.hist(dataframe['created_hour'].dropna(), bins=range(0, 25), edgecolor='black', color='cyan')
    plt.xlabel('Hour of the Day (UTC)')
    plt.ylabel('Number of Investigations')
    plt.title('Frequency Distribution of Investigation Creation Times')
    plt.xticks(range(0, 24))
    plt.savefig("../docs/charts/investigations_histogram_frequency_distribution.png")


def investigations_created_over_time_disposition_all():
    '''Number of Investigations created over time by Disposition'''
    with open("investigations_json/investigations_list.json","r",encoding="UTF-8") as infile:
        investigations_loaded = json.load(infile)
        dataframe = convert_json_to_dataframe(investigations_loaded)

    # Resample the 'created_time' to daily frequency and count the number of investigations created each day, separated by disposition
    time_series_data_by_disposition = dataframe.groupby('disposition').resample('D', on='created_time').size().reset_index(name='count')

    # Create the area chart
    plt.figure(figsize=(14, 6))
    sns.lineplot(x='created_time', y='count', hue='disposition', data=time_series_data_by_disposition, markers=True, dashes=False)
    plt.fill_between(time_series_data_by_disposition['created_time'].unique(), 
                    time_series_data_by_disposition.groupby('created_time')['count'].sum(), 
                    color='grey', alpha=0.2)
    plt.xlabel('Created Time')
    plt.ylabel('Number of Investigations')
    plt.title('Number of Investigations Created Over Time by Disposition')
    plt.legend(title='Disposition')
    plt.grid(True)
    plt.savefig("../docs/charts/investigations_created_over_time_disposition_all.png")


if __name__ == "__main__":
    # check_investigations() # Comment if don't need to call API again
    investigations_pie_chart_all_clients()
    investigations_bar_chart_all_priority()
    investigations_donut_all_clients()
    investigations_time_series_creation_all()
    investigations_time_priority_creation_all()
    investigations_histogram_frequency_distribution()
    investigations_created_over_time_disposition_all()
