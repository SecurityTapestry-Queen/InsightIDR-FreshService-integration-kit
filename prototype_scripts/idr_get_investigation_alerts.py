import requests

def getInsightInvestigation(id):
    url = 'https://us2.api.insight.rapid7.com/idr/v2/investigations/' + id + '/alerts'
    headers = {
    "X-Api-Key": "",
    "Accept-version": "investigations-preview"
    }
    params = {
    "multi-customer": True
    }

    r = requests.get(url, headers=headers, params=params)
    investigations = r.json()
    print(investigations)

ticket = 'rrn:investigation:us2:cc6da3c6-9246-4fb1-ac99-6c4eb2626663:investigation:GPGFFIG08MAJ'

getInsightInvestigation(ticket)