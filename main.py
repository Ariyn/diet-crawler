#encoding:utf-8
from __future__ import print_function

import sys
import json, codecs
import urllib2
import re
from datetime import date

print('Loading function')

header = {
	"Accept-Language":"ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4,ja;q=0.2"
}

def crawl(url="http://chains.changwon.ac.kr/wwwhome/html/mailbox/lunch.php?kind=S"):
	req = urllib2.Request(url, headers = header)
	response = urllib2.urlopen(req)
	data = response.read()
	
	data = data.decode("cp949").encode("utf-8")
	open("sample", "wb").write(data)

def parse(data):
	
	dateSearch = re.search(u"<td>\s*기간 ([0-9]{4}) 년 ([0-9]{2}) 월 ([0-9]{2}) 일에서  ([0-9]{4}) 년 ([0-9]{2}) 월 ([0-9]{2}) 일까지\s*<\/td>", data, re.S|re.M)
	if dateSearch:
		dateSearch = dateSearch.groups()
	else:
		# raise error
		pass
	firstDay = date(int(dateSearch[0]), int(dateSearch[1]), int(dateSearch[2]))
	lastDay = date(int(dateSearch[3]), int(dateSearch[4]), int(dateSearch[5]))
	# print(date(int(dateSearch[0]), int(dateSearch[1]), int(dateSearch[2])), 
	# date(int(dateSearch[3]), int(dateSearch[4]), int(dateSearch[5])))
	
	frameSearch = re.findall("<td\s*class='pad4'.+?>(.+?)</td>", data, re.S|re.M)
	frameSearch = [i.replace("<br>", "\n").replace("<br />", "\n") for i in frameSearch]
	frames = frameSearch[0::4]
	# print(len(frameSearch))
	
	retVal = {"range":(firstDay, lastDay), "월":[], "화":[], "수":[], "목":[], "금":[]}
	# retVal = {"range":(":".join(dateSearch.groups()[:3]), ":".join(dateSearch.groups()[3:])) }
	
	for index, name in zip(range(0,5), ["월", "화", "수", "목", "금"]):
		frames = frameSearch[index::5]
		
		launch, dinner = frames[2].replace(u"[중식]", "").split(u"[석식]")
		frames.pop(2)
		frames.append(launch)
		frames.append(dinner)
		
		for v in frames:
			retVal[name].append(v.encode("utf-8").replace("\n\n","\n").rstrip().lstrip())
			
		return retVal
	

def lambda_handler(event, context):
	#print("Received event: " + json.dumps(event, indent=2))
	print("value1 = " + event['key1'])
	print("value2 = " + event['key2'])
	print("value3 = " + event['key3'])
	return event['key1']  # Echo back the first key value
	#raise Exception('Something went wrong')

# print(sys.version)
# crawl()

dietData = parse(codecs.open("sample", "r", "utf-8").read())
print(dietData["range"][0].weekday(), dietData["range"][1].weekday())
for i in dietData["월"]:
	print(i,"\n")
