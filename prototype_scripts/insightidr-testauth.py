import requests

url = 'https://us2.api.insight.rapid7.com/validate'

x = requests.post(url, headers = {"X-Api-Key": "x"})

print(x.text)