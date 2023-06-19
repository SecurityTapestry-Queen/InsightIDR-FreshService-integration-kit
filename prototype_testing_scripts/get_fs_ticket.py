import requests

webhook_url = 'https://securitytapestry.freshservice.com/api/v2/tickets/'
auth = ("x", "X")
ticket_id = "493"

requests.get(webhook_url + ticket_id, auth)