import requests
import json

webhook_url = 'https://securitytapestry.freshservice.com/api/v2/tickets'

data = {
"description":"Testing Webhook with Python",
"subject":"Testing Hook",
"email":"hooktest@example.com",
"status":2,
"priority":1
}

requests.post(webhook_url, auth=('x', 'X'), data=json.dumps(data), headers= {'Content-Type': 'application/json'})