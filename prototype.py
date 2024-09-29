import json

import requests
address = 'http://localhost:11434/api/generate'

response = requests.post(address, json={
    'model': 'llama3.2',
    'prompt' : 'You are given a ticket from Jira: '
               ''
               ''
               ''
               'The ticket is supposed to fit the following criteria:'
               ''
               ''
               'Does the ticket fulfill the criteria? Answer using true or false and in JSON using a single field called "fulfills_criteria".',



    'format': 'json',
    'stream': False,
    'seed' : 42
})
response.raise_for_status()
content = json.loads(json.loads(response.content).get('response'))
print(content)
print(type(content))