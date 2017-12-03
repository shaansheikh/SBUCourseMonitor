import requests
import json
from lxml import html
import xml.etree.ElementTree as ET

def scrape(id):
	try:
		r = requests.get("http://classfind.stonybrook.edu/vufind/AJAX/JSON?method=getItemVUStatuses&itemid=" + str(id) + "&strm=1184")
	except:
		return -1000
	
	a=json.loads(r.text)["data"]
	return int(a[a.index("<SU_ENRL_AVAL>")+14:a.index("</SU_ENRL_AVAL>")])

def getinfo(id):
	if not str.isdigit(id):
		return "ERROR"
	try:
		a=requests.get("http://classfind.stonybrook.edu/vufind/Search/Results?lookfor=" + id + "&type=AllFields&view=rss")
		b=ET.fromstring(a.text).findall(".//channel//item//title")
	except:
		return "FAIL"
	if (len(b)!=1):
		return "ERROR"
	course = b[0].text
	prof=ET.fromstring(a.text).findall(".//channel//item//author")[0].text
	a = requests.get("http://classfind.stonybrook.edu/vufind/Search/Results?lookfor=" + id)
	code=html.fromstring(a.text).xpath('//div[@class="span-2"]//a//b')[0].text
	return code + ": " + course + " taught by " + prof

def statusUpdate(username,database):
	return [getinfo(str(x[0])) + " - " + str(scrape(x[0])) + " seats open" for x in database.getFollowingCourses(username)]

print "hi"
