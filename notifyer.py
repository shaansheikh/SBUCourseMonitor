from scrape import getinfo,scrape,statusUpdate
from dbaccess import AuthDatabase
from interface import Interface
import datetime
import json

config = json.loads(open("/root/SBUCourseMonitor/config.json").read())
messenger = Interface(config)

db = AuthDatabase(config["database_addr"])

for job in db.getJobs():
	seats = scrape(job[2])
	if seats > 0:
		user = db.getUserByID(job[1])[0]
		info = getinfo(str(job[2]))
		messenger.message(user[1],user[2],"Knock, knock! You course " + info + " now has " + str(seats) + " open seats. Go sign up!")
		print datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + "\t" + user[2] + "\t" + info
		db.deleteJob(job[0])
