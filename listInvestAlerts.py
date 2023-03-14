import requests
from datetime import datetime

def getInvestigationAlerts(identifier):
    url = 'https://us2.api.insight.rapid7.com/idr/v2/investigations/'+identifier+'/alerts'
    headers = {
    "X-Api-Key": "0690fa52-b1f5-458c-8c2a-4ca31f6643c9",
    "Accept-version": "investigations-preview"
    }
    params = {
    # "multi-customer": True,
    }

    r = requests.get(url, headers=headers, params=params)
    alerts = r.json()["data"]
    print(alerts)

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
    

print("Getting Investigation Alerts" + "\n")
getInvestigationAlerts('2daa60d2-da04-444a-84b8-d0c36a59d6ec')
