#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Test Script to GET evidence from Investigation in InsightIDR"""

import ast
import json
import requests

def get_investigation_evidence(rrn):
    """Main Method"""
    url = 'https://us2.api.insight.rapid7.com/idr/v1/restricted/investigations/' + rrn + '/evidence'
    headers = {"X-Api-Key": ""}
    request = requests.get(url, headers=headers, timeout=30)
    data = request.json()['indicator_occurrences']
    for i,evidences in enumerate(data):
        evidence = evidences['evidence'][1]['details']['content']
        # unescaped_evidence = str(evidence).encode().decode('unicode_escape')
        # twice_unescaped = unescaped_evidence.replace('\\','',1)
        ast_evaled = ast.literal_eval(evidence)
        print(ast_evaled)
        print('\n\n' + f'Evidence {i+1}' + '\n\n')
        # print(json.dumps(evidence, indent=4) + '\n\n' + f'Evidence {i+1}' + '\n\n')
        # print(json.dumps(unescaped_evidence, indent=4) + '\n\n' + f'Evidence {i+1}' + '\n\n')
        # print(json.dumps(twice_unescaped, indent=4) + '\n\n' + f'Evidence {i+1}' + '\n\n')
        with open(f'evidence/evidence-{i}.json', 'w', encoding='UTF-8') as evidence_file:
            json.dump(ast_evaled, evidence_file, indent=4)
        # print(json.dumps(unescaped_evidence, indent=4) + '\n\n' + f'Evidence {i+1}' + '\n\n')
        # with open(f'evidence/evidence-{i}.json', 'w', encoding='UTF-8') as evidence_file:
        #     json.dump(twice_unescaped, evidence_file, indent=4)

TICKET_ANGRY_IP_SCANNER = 'rrn:investigation:us2:cc6da3c6-9246-4fb1-ac99-6c4eb2626663:investigation:BBDC2MA7X3SY'

TICKET_HONEYPOT_CONNECTION = 'rrn:investigation:us2:cc6da3c6-9246-4fb1-ac99-6c4eb2626663:investigation:UMS89TFB80D8'

get_investigation_evidence(TICKET_ANGRY_IP_SCANNER)
# get_investigation_evidence(TICKET_HONEYPOT_CONNECTION)
