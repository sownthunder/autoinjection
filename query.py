import time
import datetime
import sqlite3
from main import autoinjection
import tempfile
import os

autoSqli = autoinjection()

valueSet = []

filestream = open("txt\\taskidlist.txt",'r')
taskidlist = filestream.readlines()

while True:
	for taskid in taskidlist:
		staUrl = "http://127.0.0.1:8775/scan/%s/status" % taskid.rstrip('\n')
		dataUrl = "http://127.0.0.1:8775/scan/%s/data" % taskid.rstrip('\n')
		status = autoSqli.GetStatus(staUrl)

		if taskid not in valueSet and status == "terminated":
			valueSet.append(taskid)
			autoSqli.GetData(dataUrl)

	if len(valueSet) == len(taskidlist):
		break
	time.sleep(3)

filestream.close()
