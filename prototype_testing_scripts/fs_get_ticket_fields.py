import requests

webhook_url = 'https://securitytapestry.freshservice.com/api/v2/ticket_form_fields'
auth = ("", "X")

requests.get(webhook_url, auth)