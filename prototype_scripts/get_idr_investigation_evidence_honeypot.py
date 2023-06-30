#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Test Script to GET evidence from Investigation in InsightIDR"""
# honeypot evidence is different

import json
import requests

def get_investigation_evidence(rrn):
    """Main Method"""
    url = 'https://us2.api.insight.rapid7.com/idr/v1/restricted/investigations/' + rrn + '/evidence'
    headers = {"X-Api-Key": ""}
    request = requests.get(url, headers=headers, timeout=30)
    data = request.json()
    if data["indicator_occurrences"][0]["evidence"][0]["type"] == "HoneypotConnectionEvidence":
        pointer = data["indicator_occurrences"][0]["evidence"]
        print(json.dumps(pointer, indent=4))

TICKET = 'rrn:investigation:us2:cc6da3c6-9246-4fb1-ac99-6c4eb2626663:investigation:' + 'UMS89TFB80D8'

get_investigation_evidence(TICKET)
