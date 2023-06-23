import requests
from datetime import datetime

def getInvestigations():
    url = 'https://us2.api.insight.rapid7.com/idr/v2/investigations'
    headers = {
    "X-Api-Key": "",
    "Accept-version": "investigations-preview"
    }
    params = {
    "statuses": "OPEN,INVESTIGATING",
    "multi-customer": True,
    "sources": "ALERT",
    "priorities": "CRITICAL,HIGH,MEDIUM,LOW"
    }

    r = requests.get(url, headers=headers, params=params)
    investigations = r.json()["data"]

    # for i in investigations:
    #     print(
    #     "Title: " + i["title"] + "\n"
    #     "Disposition: " + i["disposition"] + "\n"
    #     "Date Created: " + i["created_time"] + "\n"
    #     "Last Accessed: " + i["last_accessed"]
    #      )
    #     if i["assignee"] is None:
    #         print("No Assignee" + "\n")
    #     else:
    #         print("Assignee: " + i["assignee"]["name"] + "\n")
    for i in investigations:
        print(i)

print("Getting Investigations" + "\n")
getInvestigations()
