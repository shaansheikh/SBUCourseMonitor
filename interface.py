import requests
import json
from twilio.rest import Client

class Interface:

	def __init__(self,configin):
		self.config = configin

	def message(self,medium,username,message):
		if medium == 0:
			return self.messageKik(username,message)
		elif medium == 1:
			return self.messageFB(username,message)
		elif medium == 2:
			self.messageSMS(username,message)

	def messageSMS(self,username,message):
		account_sid = self.config["twilio_sid"]
		auth_token = self.config["twilio_auth_token"]

		client = Client(account_sid, auth_token)

		message = client.messages.create(
		    to=username, 
		    from_="+16314961738",
		    body=message)

	def yesnomessage(self,medium,username,message):
		if medium == 0:
			self.yesnomessageKik(username,message)
		elif medium == 1:
			self.yesnomessageFB(username,message)
		else:
			self.messageSMS(username, message + " Yes or No?")

	def messageKik(self,username,message):
		return requests.post(
			'https://api.kik.com/v1/message',
			auth=(self.config["kik_usr"], self.config["kik_apikey"]),
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
		
	def yesnomessageKik(self,username,message):
		return requests.post(
			'https://api.kik.com/v1/message',
			auth=(self.config["kik_usr"], self.config["kik_apikey"]),
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


	def messageFB(self,userid,message):

		headers = {'Content-Type': 'application/json',}
		data = '{"recipient":{"id":'+str(userid)+'},"message":{"text":"'+message+'"},"quick_replies":[{"content_type":"text","title":"<BUTTON_TEXT>","payload":"<STRING_SENT_TO_WEBHOOK>"}]}'
		return requests.post('https://graph.facebook.com/v2.6/me/messages?access_token='+self.config["fb_token"], headers=headers, data=data)

	def yesnomessageFB(self,userid,message):
		headers = { 'Content-Type': 'application/json',}

		data = '{ "recipient":{ "id":'+str(userid)+'},"message":{ "attachment":{ "type":"template","payload":{ "template_type":"button","text":"'+message+'","buttons":[ { "type":"postback","title":"Yes","payload":"Yes" },{ "type":"postback","title":"Nope","payload":"Nope"}]}}}}'
		requests.post('https://graph.facebook.com/me/messages?access_token='+self.config["fb_token"],headers=headers,data=data)
