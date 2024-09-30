import json

import requests
address = 'http://localhost:11434/api/generate'


def check_criteria(ticket: str, criteria: str):
    """Check if a ticket fulfills a certain criteria"""

    response = requests.post(address, json={
        'model': 'llama3.2',
        'prompt' : 'You are given a ticket from Jira: "'+ticket+'"\n'
                   'The ticket is supposed to fit the following criteria:"'+criteria+'"'
                   'Does the ticket fulfill the criteria? Answer using true or false and in JSON using a boolean field "fulfills_criteria" and another field "explanation" in which it is explained why the given requirement is not fulfilled.',
        'format': 'json',
        'stream': False,
        'seed' : 42
    })
    response.raise_for_status()
    content = json.loads(json.loads(response.content).get('response'))
    return response.content

with open('./criterion/', mode='r') as criteria_file, open('./ticket', mode='r') as ticket_file:
    for line in criteria_file:
        print(check_criteria(ticket_file.read(), line))