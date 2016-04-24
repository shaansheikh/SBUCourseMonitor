from scrape import getinfo,scrape,statusUpdate
from dbaccess import AuthDatabase
from interface import message,yesnomessage,messageFB

db = AuthDatabase("/root/SBUCourseMonitor/sbucourse.db")

print db.getJobs()