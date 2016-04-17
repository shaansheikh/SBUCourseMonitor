import requests
import json

def message(username,message):
	return requests.post(
		'https://api.kik.com/v1/message',
		auth=('shaanbot', 'a024ef5e-627c-4166-9fb1-2093cba4f544'),
		headers={
			'Content-Type': 'application/json'
		},
		data=json.dumps({
			'messages': [
				{
					'body':message, 
					'to': username, 
					'type': 'text'
				}
			]
		})
	)
	
def yesnomessage(username,message):
	return requests.post(
		'https://api.kik.com/v1/message',
		auth=('shaanbot', 'a024ef5e-627c-4166-9fb1-2093cba4f544'),
		headers={
			'Content-Type': 'application/json'
		},
		data=json.dumps({
        	"messages": [
        		{
        			"type": "text",
        			"to": username,
        			"body": message,
        			"keyboards": [
        				{
        					"to": username,
        					"type": "suggested",
        					"responses": [
        						{
        							"type": "text",
        							"body": "Yes"
        						},
        						{
        							"type": "text",
        							"body": "Nope"
        						}
        					]
        				}
        			]
        		}
        	]
        }))