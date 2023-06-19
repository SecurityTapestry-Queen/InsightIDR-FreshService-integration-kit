import requests
import json

ticket = 'rrn:investigation:us2:cc6da3c6-9246-4fb1-ac99-6c4eb2626663:investigation:296BUI5MX7I9'
ID = "66"

def getInvestigationComments(id):
    url = 'https://us2.api.insight.rapid7.com/idr/v1/comments'
    headers = {
    "X-Api-Key": "x",
    "Accept-version": "comments-preview"
    }
    params = {
    "multi-customer": True,
    "target": id
    }

    r = requests.get(url, headers=headers, params=params)
    comments = r.json()
    # print(comments)
    global c
    for c in comments["data"]:
        if c["body"] is None:
            continue
        else:
            postCommentsToFS(ID)

def postCommentsToFS(fsID):
    webhook_url = 'https://securitytapestry.freshservice.com/api/v2/tickets/' + fsID + '/notes'

    data = {
        "body": c["body"],
        "private": False
    }

    requests.post(webhook_url, auth=('x', 'X'), data=json.dumps(data), headers= {'Content-Type': 'application/json'})


getInvestigationComments(ticket)
