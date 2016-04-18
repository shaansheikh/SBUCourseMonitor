import flask
import requests
import json
from flask import Flask,render_template,request,send_from_directory,session,flash,redirect
from OpenSSL import SSL
from scrape import getinfo,scrape
from dbaccess import AuthDatabase
from interface import message,yesnomessage,messageFB

app = Flask(__name__)
db = AuthDatabase("sbucourse.db")
app.secret_key="A0Zr98j/3yX R~XHH!jmN]LWX/,?RT"

@app.route('/', methods=['GET', 'POST'])
def index():

	if request.data:
		print request.data
		data = json.loads(request.data)
		medium = -1
		if "messages" in data:
			medium = 0
			for incomingmsg in data["messages"][:1]:
				username = incomingmsg["from"].encode('ascii', 'ignore')
				payload = incomingmsg["body"].encode('ascii', 'ignore')
		elif "entry" in data:
			medium = 1
			username = data["entry"][0]["messaging"][-1]["sender"]["id"]
			if "message" in data["entry"][0]["messaging"][-1] and "text" in data["entry"][0]["messaging"][-1]["message"]:
				payload = data["entry"][0]["messaging"][-1]["message"]["text"].encode('ascii', 'ignore')
			elif "postback" in data["entry"][0]["messaging"][-1]:
				payload = data["entry"][0]["messaging"][-1]["postback"]["payload"]
			else:
				message(1,username,"(y)")
				return "not message or postback"

		else:
			return "invalid request"

		if payload.lower().replace(" ","") =="removeme":
			db.reset(username)
			message(medium,username,"YOU HAVE BEEN REMOVED FROM DATABASE. You will no longer recieve updates.")
			return "hi"
			
		user = db.isUser(username)
		print user
		if len(user) == 0:
			message(medium,username,"Hello! Have a class you want to take that's full? I'll monitor it for you and let you know when it opens up!")
			message(medium,username,"Why don't you start by telling me the five digit id of the section you want.")
			db.addUser(username)
			return "hi"
		else:
			
			state = user[0][3]
			if state == 1:
				
				classinfo = getinfo(payload)
				if classinfo == "ERROR":
					message(medium,username,"Hmmm, that doesn't seem to be a valid course code. You can find the course code of your section on SOLAR. It should be a five digit number. Reply with the number when you find it.")
					return "hi"

				elif classinfo == "FAIL":
					message(medium,username,"Could not check class status :( Is Classfind down?")
					db.reset(username)
					return "hi"

				else:
					db.addTemp(username,payload)
					message(medium,username,"Okay! I found the following class:")
					message(medium,username, classinfo)
					yesnomessage(medium,username,"Is this the right class?")
					db.changeState(username,2)
					return "hi"
		  
			elif state == 2:
				if payload == "Nope":
					message(medium,username,"Oops! Why don't you tell me the 5 digit ID of the class you're actually looking for. You can find the course code of your section on SOLAR.")
					db.changeState(username,1)
					return "hi"
				elif payload == "Yes":
					seats = scrape(db.getTemp(username))
					if seats > 0:
						message(medium,username,"Good news! Your class has " + str(seats) + " open seats, so you can go sign up now! If you have the id of another course that's closed that you'd like to track, let me know!")
						db.changeState(username,1)
						return "hi"				
					else:
						message(medium,username,"You're all set! I'll monitor your course message you here if a seat in your class opens up.")
				else:
					message(medium,username,"Pick yes or no")
					yesnomessage(medium,username,"Is this the right class?")
					return "hi"


	return '<!DOCTYPE HTML><html lang="en-US"><head><meta charset="UTF-8"><meta http-equiv="refresh" content="1;url=http://shaansweb.com"><script type="text/javascript">window.location.href = "http://shaansweb.com"</script><title>Page Redirection</title></head>'



def main():
	app.debug = True
	app.run(host='0.0.0.0', port=4000, ssl_context=("/etc/letsencrypt/live/shaansweb.com/fullchain.pem","/etc/letsencrypt/live/shaansweb.com/privkey.pem"))
	print session

if __name__ == '__main__':
	main()
	pass

