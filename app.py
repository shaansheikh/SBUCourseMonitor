import flask
import requests
import json
from flask import Flask,render_template,request,send_from_directory,session,flash,redirect
from OpenSSL import SSL
from scrape import getinfo
from dbaccess import AuthDatabase
from interface import message

app = Flask(__name__)
db = AuthDatabase
app.secret_key="A0Zr98j/3yX R~XHH!jmN]LWX/,?RT"

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.data:
		data = json.loads(request.data)
		username = data["messages"][0]["from"].encode('ascii', 'ignore')
		message = data["messages"][0]["body"].encode('ascii', 'ignore')

		message(username,message)


	return "hi"



def main():
	app.debug = True
	app.run(host='0.0.0.0', port=4000, ssl_context=("/etc/letsencrypt/live/shaansweb.com/fullchain.pem","/etc/letsencrypt/live/shaansweb.com/privkey.pem"))
	print session

if __name__ == '__main__':
	main()
	pass

