import requests

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
    for c in comments["data"]:
        print(c)

ticket = 'rrn:investigation:us2:cc6da3c6-9246-4fb1-ac99-6c4eb2626663:investigation:296BUI5MX7I9'

getInvestigationComments(ticket)