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

ticket = 'rrn:investigation:us2:787bed8a-7ac8-41bc-8337-5f093af0e025:investigation:JDW390DIWSWS'

getInsightInvestigation(ticket)