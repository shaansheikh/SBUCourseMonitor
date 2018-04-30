import flask
import requests
import json
from flask import Flask,render_template,request,send_from_directory,session,flash,redirect
from OpenSSL import SSL
from scrape import getinfo,scrape,statusUpdate
from dbaccess import AuthDatabase
from interface import Interface
import threading
import json

config = json.loads(open("./config.json").read())

app = Flask(__name__)
db = AuthDatabase(config["database_addr"])
app.secret_key=config["secretkey"]
messenger = Interface(config)


def lookup(medium,username,payload):
	classinfo = getinfo(payload)
	if classinfo == "ERROR":
		messenger.message(medium,username,"Hmmm, that doesn't seem to be a valid course code. You can find the course code of your section on SOLAR. It should be a five digit number. Reply with the number when you find it.")
		db.changeState(username,1)

	elif classinfo == "FAIL":
		messenger.message(medium,username,"Could not check class status :( Is Classfind down?")
		db.changeState(username,1)

	else:
		db.addTemp(username,payload)
		messenger.message(medium,username,"Okay, I found the following class:")
		messenger.message(medium,username, classinfo)
		messenger.yesnomessage(medium,username,"Is this the right class?")
		db.changeState(username,2)

def seatcheck(medium,username):
	seats = scrape(db.getTemp(username))
	if seats > 0:
		messenger.message(medium,username,"Good news! Your class has " + str(seats) + " open seats, so you can go sign up now! If you have the ID of another course that's closed that you'd like to track, let me know!")
		db.changeState(username,1)

	elif seats > -1000:
		messenger.message(medium,username,"You're all set. I'll monitor your course and message you here if a seat in your class opens up.")
		messenger.message(medium,username,"Anything else I can help you with? You can say 'commands' for a list of commands I understand.")
		temp = db.getTemp(username)
		db.addJob(username,temp)
		db.changeState(username,0)
	else:
		messenger.message(medium,username,"Couldn't figure out how many seats open. Is classfind down?")
		db.changeState(username,2)

def statusupdatethread(medium,username):
	updates = statusUpdate(username,db)
	if len(updates) ==0:
		messenger.message(medium,username,"I'm not monitoring any classes for you. Type 'add class' if you'd like me too")
	for update in updates:
		messenger.message(medium,username,update)
	db.changeState(username,0)

@app.route('/', methods=['GET', 'POST'])
def index():
	data = None
	if request.data:
		data = json.loads(request.data)
	elif request.form:
		data = request.form
	
	medium = -1
	if "messages" in data:
		medium = 0
		if len(data["messages"])>1:
			messenger.message(0,"shaansweb",str(messages[1:]))
		for incomingmsg in data["messages"][:1]:
			username = incomingmsg["from"].encode('ascii', 'ignore')
			if "body" in incomingmsg:
				payload = incomingmsg["body"].encode('ascii', 'ignore')
			else:
				print "invalid!"
				return "invalid"
			print username + "\t" + payload
	elif "X-Hub-Signature" in request.headers:
		medium = 1
		username = data["entry"][0]["messaging"][-1]["sender"]["id"]
		if "message" in data["entry"][0]["messaging"][-1] and "text" in data["entry"][0]["messaging"][-1]["message"]:
			payload = data["entry"][0]["messaging"][-1]["message"]["text"].encode('ascii', 'ignore')
		elif "postback" in data["entry"][0]["messaging"][-1]:
			payload = data["entry"][0]["messaging"][-1]["postback"]["payload"]
		else:
			messenger.message(1,username,"(y)")
			return "not message or postback"
	elif "SmsMessageSid" in data:
		medium = 2
		username = data["From"]
		payload = data["Body"].encode('ascii', 'ignore').lower().replace(" ","")


	else:
		return "invalid request"

	if payload.lower().replace(" ","") =="removeme":
		db.reset(username)
		messenger.message(medium,username,"YOU HAVE BEEN REMOVED FROM DATABASE. You will no longer recieve updates.")
		return "hi"

	if username=="shaansweb" and payload.lower().replace(" ","")=="getusers":
		users = db.getUsers()
		retstr=str(len(users))+ " users: "
		for user in users:
			retstr=retstr+user[0]+", "			
		messenger.message(0,"shaansweb",retstr)
		return "hi"
		
	user = db.isUser(username)
	if len(user) == 0:
		messenger.message(medium,username,"Hello! Have a class you want to take that's full? I'll monitor it for you and let you know when it opens up!")
		messenger.message(medium,username,"Why don't you start by telling me the five digit ID of the section you want.")
		#FIX THIS WHEN FB IS APPROVED
		db.addUser(username)
		return "hi"
	else:
		
		state = user[0][3]
		if state == 1:
			if payload.lower().replace(" ","") == "cancel":
				messenger.message(medium,username,"ok")
				db.changeState(username,0)
				return "Hello"
			
			db.changeState(username,4)
			thread = threading.Thread(target=lookup,args=(medium,username,payload))
			thread.start()
			return "hi"

	  
		elif state == 2:
			if payload.lower() == "nope" or payload.lower()=="no":
				messenger.message(medium,username,"Oops! Why don't you tell me the 5 digit ID of the class you're actually looking for. You can find the course code of your section on SOLAR.")
				db.changeState(username,1)
				return "hi"
			elif payload.lower() == "yes":
				db.changeState(username,4)
				thread = threading.Thread(target=seatcheck,args=(medium,username))
				thread.start()
				return "hi"
			else:
				messenger.message(medium,username,"Pick yes or no")
				messenger.yesnomessage(medium,username,"Is this the right class?")
				return "hi"
		elif state == 0:
			if payload.lower().replace(" ","") == "commands":
				if medium == 0:
					messenger.message(medium,username,"""Remove me - Delete all records of you from the database.
Add class - Add another section to follow.
Status update - See which courses I'm currently monitoring for open seats for you.
Commands - Show this menu.
About - Information
Feedback - Submit feedback or report a problem
""")
				else:
					messenger.message(medium,username,"Remove me - Delete all records of you from the database.")
					messenger.message(medium,username,"Add class - add another section to follow.")
					messenger.message(medium,username,"Status update - See which courses I'm currently monitoring for open seats for you.")
					messenger.message(medium,username,"Commands - show this menu.")						
					messenger.message(medium,username,"About - Information")
				return "hi"
			elif payload.lower().replace(" ","") == "addclass":
				messenger.message(medium,username,"Tell me the five digit code of the class")
				db.changeState(username,1)
				return "hi"
			elif payload.lower().replace(" ","") == "statusupdate":
				db.changeState(username,4)
				thread = threading.Thread(target=statusupdatethread,args=(medium,username))
				thread.start()
				return "hi"
			elif payload.lower().replace(" ","")=="about":
				messenger.message(medium,username,"I was created by Shaan Sheikh at a YHack 2017F!")
				messenger.message(medium,username,"If you have any questions or want to report any problems, use the feedback command or email shaan.sheikh@stonybrook.edu")
				return "hi"
			elif payload.lower().replace(" ","")=="feedback":
				messenger.message(medium,username,"Your next message to me will be recorded as feedback. Use this to report any issues")
				messenger.message(medium,username,"If you don't want to submit any feedback, just say cancel")
				db.changeState(username,3)
				return "hi"
			else:
				messenger.message(medium,username,"Sorry, I don't understand what you said. Humans are hard to understand. I'm still getting the hang of it")
				messenger.message(medium,username,"Say 'commands' for a list of things I can understand")
				return "hi"
		elif state==3:
			if payload.lower().replace(" ","")=="cancel":
				messenger.message(medium,username,"ok, canceled")
				db.changeState(username,0)
				return "hi"
			else:
				messenger.message(0,"shaansweb",str(username) + ": " + payload)
				messenger.message(medium,username,"Thanks, you feedback was recorded. We'll message you here if we have any questions")
				db.changeState(username,0)
				return "hi"
		elif state==4:
			messenger.message(medium,username,"hang tight, I'm still thinking")
		else:
			messenger.message(medium,username,"You seem to be in an invalid state. Email shaan.sheikh@stonybrook.edu")


	return '<!DOCTYPE HTML><html lang="en-US"><head><meta charset="UTF-8"><meta http-equiv="refresh" content="1;url=http://shaansweb.com"><script type="text/javascript">window.location.href = "http://shaansweb.com"</script><title>Page Redirection</title></head>'



def main():
	app.debug = True
	app.run(host='0.0.0.0', port=config["serverport"], ssl_context=(config["cert_addr"],config["key_addr"]))
	print session

if __name__ == '__main__':
	main()
	pass

