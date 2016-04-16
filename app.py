import flask
import requests
import json
from flask import Flask,render_template,request,send_from_directory,session,flash,redirect
from OpenSSL import SSL

app = Flask(__name__)
app.secret_key="A0Zr98j/3yX R~XHH!jmN]LWX/,?RT"

@app.route('/', methods=['GET', 'POST'])
def index():
	print json.loads(request.data)
	fromid = json.loads(request.data)["messages"][0]["from"]
	print fromid

	a = requests.post(
		'https://api.kik.com/v1/message',
		auth=('shaanbot', 'a024ef5e-627c-4166-9fb1-2093cba4f544'),
		headers={
			'Content-Type': 'application/json'
		},
		data=json.dumps({
			'messages': [
				{
					'body': 'I like ike', 
					'to': fromid, 
					'type': 'text'
				}
			]
		})
	)
	return "hi"



def main():
	app.debug = True
	app.run(host='0.0.0.0', port=4000, ssl_context=("/etc/letsencrypt/live/shaansweb.com/cert.pem","/etc/letsencrypt/live/shaansweb.com/privkey.pem"))
	print session

if __name__ == '__main__':
	main()
	pass

