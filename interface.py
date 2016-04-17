import requests
import json

def message(medium,username,message):
	if medium == 0:
		messageKik(username,message)
	else:
		messageFB(username,message)

def yesnomessage(medium,username,message):
	if medium == 0:
		yesnomessageKik(username,message)
	else:
		yesnomessageFB(username,message)

def messageKik(username,message):
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
	
def yesnomessageKik(username,message):
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
	data = '{"recipient":{"id":'+userid+'},"message":{"text":"'+message+'"}}'
	requests.post('https://graph.facebook.com/v2.6/me/messages?access_token=EAAWFfyr0QmMBAIlTe6EOCtZBzCH3aT2HVZCFLSn8V77bjBVnXCet9IztJ7Kzh6QuD5wa4qj4ZB4ZAdRZBOqlqZC1K0tL4DhYl3UKGoWSw3xII1ID6qbYAp2omEaPNYHrW3erGQUDuarKu11KYM7B9Iraot08bXDI56ivrlxQULzgZDZD', headers=headers, data=data)

def yesnomessageFB(userid,message):
	headers = { 'Content-Type': 'application/json',}

	data = '{ "recipient":{ "id":'+userid+'},"message":{ "attachment":{ "type":"template","payload":{ "template_type":"button","text":"What do you want to do next?","buttons":[ { "type":"postback","title":"Yes","payload":"Yes" },{ "type":"postback","title":"Nope","payload":"Nope"}]}}}}'
	requests.post('https://graph.facebook.com/me/messages?access_token=EAAWFfyr0QmMBAIlTe6EOCtZBzCH3aT2HVZCFLSn8V77bjBVnXCet9IztJ7Kzh6QuD5wa4qj4ZB4ZAdRZBOqlqZC1K0tL4DhYl3UKGoWSw3xII1ID6qbYAp2omEaPNYHrW3erGQUDuarKu11KYM7B9Iraot08bXDI56ivrlxQULzgZDZD',headers=headers,data=data)