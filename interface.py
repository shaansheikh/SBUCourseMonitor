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


def messageFB(userid,message):
	headers = {'Content-Type': 'application/json',}
	data = '{"recipient":{"id":'+str(userid)+'},"message":{"text":"'+message+'"}}'
	requests.post('https://graph.facebook.com/v2.6/me/messages?access_token=EAAWFfyr0QmMBAIlTe6EOCtZBzCH3aT2HVZCFLSn8V77bjBVnXCet9IztJ7Kzh6QuD5wa4qj4ZB4ZAdRZBOqlqZC1K0tL4DhYl3UKGoWSw3xII1ID6qbYAp2omEaPNYHrW3erGQUDuarKu11KYM7B9Iraot08bXDI56ivrlxQULzgZDZD', headers=headers, data=data)