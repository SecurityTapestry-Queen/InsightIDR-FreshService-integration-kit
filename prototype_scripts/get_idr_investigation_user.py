import requests

def getInsightInvestigation(id):
    url = 'https://us2.api.insight.rapid7.com/idr/v2/investigations/' + id
    headers = {
    "X-Api-Key": "",
    "Accept-version": "investigations-preview"
    }
    # params = {
    # "multi-customer": True
    # }

    r = requests.get(url, headers=headers)
    investigations = r.json()
    print(investigations)

ticket = '2f8e7f2e-1266-470e-ac3d-92af80e836b4'

getInsightInvestigation(ticket)