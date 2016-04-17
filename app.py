import flask
import requests
import json
from flask import Flask,render_template,request,send_from_directory,session,flash,redirect
from OpenSSL import SSL
from scrape import getinfo
from dbaccess import AuthDatabase
from interface import message,yesnomessage

app = Flask(__name__)
db = AuthDatabase("sbucourse.db")
app.secret_key="A0Zr98j/3yX R~XHH!jmN]LWX/,?RT"

@app.route('/', methods=['GET', 'POST'])
def index():
	print "hola"
	if request.data:
		print request.data
		data = json.loads(request.data)
		medium = -1
		if "messages" in data:
			medium = 0
			for incomingmsg in data["messages"][:1]:
				username = incomingmsg["from"].encode('ascii', 'ignore')
				payload = incomingmsg["body"].encode('ascii', 'ignore')
		else:
			medium = 1
			username = data["entry"][0]["messaging"][-1]["sender"]["id"]
			payload = data["entry"][0]["messaging"][-1]["message"]["text"]
			print username
			print payload
			requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=EAAWFfyr0QmMBAIlTe6EOCtZBzCH3aT2HVZCFLSn8V77bjBVnXCet9IztJ7Kzh6QuD5wa4qj4ZB4ZAdRZBOqlqZC1K0tL4DhYl3UKGoWSw3xII1ID6qbYAp2omEaPNYHrW3erGQUDuarKu11KYM7B9Iraot08bXDI56ivrlxQULzgZDZD",data={"recipient":{"id":username},"message":{"text":payload}})
			return "a"
			
		user = db.isUser(username)
		if len(user) == 0:
			message(username,"Hello! Have a class you want to take that's full? I'll monitor it for you and let you know when it opens up! Why don't you start by telling me the five digit id of the section you want.")
			db.addUser(username)
			return "hi"
		else:
			state = user[0][3]
			if state == 1:
				classinfo = getinfo(payload)
				if classinfo == "ERROR":
					message(username,"Hmmm, that doesn't seem to be a valid course code. You can find the course code of your section on SOLAR. It should be a five digit number. Reply with the number when you find it.")
					return "hi"
				else:
					message(username,"Okay! I found the following class:")
					message(username, classinfo)
					yesnomessage(username,"Is this the right class?")
					db.changeState(username,2)
					return "hi"
		  
			elif state == 2:
				if payload == "Nope":
					message(username,"Oops! Why don't you tell me the 5 digit ID of the class you're actually looking for. You can find the course code of your section on SOLAR.")
					db.changeState(username,1)
					return "hi"
				elif payload == "Yes":
					message(username,"I didn't think this through")
				else:
					message(username,"Pick yes or no")
					yesnomessage(username,"Is this the right class?")
					return "hi"


	return "hi"



def main():
	app.debug = True
	app.run(host='0.0.0.0', port=4000, ssl_context=("/etc/letsencrypt/live/shaansweb.com/fullchain.pem","/etc/letsencrypt/live/shaansweb.com/privkey.pem"))
	print session

if __name__ == '__main__':
	main()
	pass

