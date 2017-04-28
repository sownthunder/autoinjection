import requests
import re
import urlparse
import getopt
import json
import sys
import os

newUrl = ''
scanUrl = ''
delUrl = ''
staUrl = ''
dataUrl = ''
baseUrl = 'http://127.0.0.1:8775'
#start-up the server on background
server = os.popen(r'server.py')

#open urlList.txt and read urls
f = open("urllist.txt",'r')
urlList = f.readlines()

class autoinjection():
	def __init__(self):
		#self.taskInfo is a dictionary looks like {taskname:[taskId,taskStatus]}
		self.taskInfo = dict()

	def usage(self):
		print ""
		print "Options:"
		print "  new        /task/new              build a new task"
		print "  scan       /scan/<taskid>         begin to scan target url"
		print "  delete     /task/<taskid>/delete  delete a scan task"
		print "  status     /scan/<taskid>/status  check the task status"
		print "  data       /scan/<taskid>/data    check the task result"
		print "  stop       /scan/<taskid>/stop    stop the task"

	def ShowTaskId(self):
		print " ------------ ------------------ ------------"
		print "|  taskname  |       taskid     |   status   |"
		print " ------------ ------------------ ------------"
		for taskname in self.taskInfo:
			staUrl = baseUrl + "/scan/%s/status" % self.taskInfo[taskname][0]
			taskStatus = GetStatus(staUrl)
			self.taskInfo[taskname][1] = taskStatus
			print "|{:^11}".format(taskname),"|{:^17}".format(self.taskInfo[taskname][0]),"|{:^11}".format(self.taskInfo[taskname][1]),"|"
			print " ------------ ------------------ ------------"

	def GetTaskId(self,newUrl):
		r = requests.get(newUrl)
		info = r.json()
		taskid = info["taskid"]
		r.close()
		return taskid

	def GetStatus(self,staUrl):
		r = requests.get(staUrl)
		info = r.json()
		if info["success"]:
			status = info["status"]
		else:
			status = "error"
		r.close()
		return status

	def BeginScan(self,scanUrl,targetUrl):
		try:
			r = requests.post(scanUrl,data=json.dumps({'url':targetUrl}),headers={'Content-Type':'application/json'})
			info = r.json()
		except:
			print "[!]start task failed!"
			return 0
		else:
			if info["success"]:
				print ""
				print "[!]task begin to run!"
				print "[+]engineid: %s" % info["engineid"]
				print "[+]success: %s" % info["success"]
				print ""
				return 1
			else:
				print ""
				print "[!]task run failed!"
				print ""
				return 0

	def multiStart(self,*taskNameList):
		for taskName in taskNameList[0]:
			taskName.strip()
			beginTaskName = int(taskName.split('-')[0])
			endTaskName = int(taskName.split('-')[-1])
			while beginTaskName != endTaskName+1:
				taskId = self.taskInfo[beginTaskName][0]
				taskStatus = self.taskInfo[beginTaskName][1]
				if taskStatus == "running":
					print "[!]this task has been started,please be patience."
				else:
					scanUrl = baseUrl + '/scan/%s/start' % taskId
					if BeginScan(scanUrl,urlList[0]):
						urlList.pop(0)

				beginTaskName += 1

	def DelTask(self,delUrl):
		r = requests.get(delUrl)
		info = r.json()
		if info["success"]:
	 		print ""
			print "[!]task has been delete!"
			print ""
			return 1
		else:
			print ""
			print "[!]task delete failed!"
			print "[+]message: %s" % info["message"]
			print ""
			return 0

	def StopScan(self,stopUrl):
		r = requests.get(stopUrl)
		info = r.json()

		if info["success"]:
			print ""
			print "[!]stop task success!"
			print ""
		else:
			print ""
			print "[!]stop task failed!"
			print "[+]message: %s" % info["message"]
			print ""

	def GetData(self,dataUrl):
		r = requests.get(dataUrl)
		info = r.json()
		try:
			if info["success"] and info["data"]:
				print ""
				print "[+]url: %s" % info["data"][0]["value"]["url"]
				print "[+]query: %s" % info["data"][0]["value"]["query"]  #ID=151
				print "[+]data: %s" % info["data"][0]["value"]["data"]  #None

				print "[+]dbms: %s" % info["data"][1]["value"][0]["dbms"]  #None
				print "[+]suffix: %s" % info["data"][1]["value"][0]["suffix"]  # AND '[RANDSTR]'='[RANDSTR]
				print "[+]dbms_version: %s" % info["data"][1]["value"][0]["dbms_version"]  #None
				print "[+]prefix: %s" % info["data"][1]["value"][0]["prefix"]  #'
				print "[+]place: %s" % info["data"][1]["value"][0]["place"]  #GET
				print "[+]os: %s" % info["data"][1]["value"][0]["os"]
				print "[+]parameter %s" % info["data"][1]["value"][0]["parameter"]  #ID
				for Injection_type in info["data"][1]["value"][0]["data"]:
					print "---------------INJECTION    TYPE    %s-----------------------" % Injection_type
					print "[+]title: %s" % info["data"][1]["value"][0]["data"][Injection_type]["title"]
					print "[+]payload: %s" % info["data"][1]["value"][0]["data"][Injection_type]["payload"]
					print ""
					print "[+]error: %s" % info["error"]
					print ""
			elif not info["data"]:
				print ""
				print "[!]this site are unvunlerable!"
				print ""
			else:
				print ""
				print "[!]Injection failed!"
				print "[+]message: %s" % info["message"]
				print ""
		except:
			print "[!]please run task before check the result!"


def main():
	autoSqli = autoinjection()
	autoSqli.usage()

	tasknumber = 1
	while True:
		try:
			parameter = raw_input("[+]Input command:")
		except:
			server.close()
			sys.exit(2)
		if parameter == 'new':
			for n in range(0,len(urlList)):
				newUrl = baseUrl + "/task/new"
				taskId = autoSqli.GetTaskId(newUrl)

				staUrl = baseUrl + '/scan/%s/status' % taskId
				taskStatus = autoSqli.GetStatus(staUrl)
				autoSqli.taskInfo[tasknumber] = [taskId,taskStatus]

				tasknumber = tasknumber + 1

		elif parameter == 'scan' and self.taskInfo:
			ShowTaskId()
			while True:
				try:
					taskNameString = raw_input("[+]Input taskname:")
					taskNameList = taskNameString.split(",")
					multiStart(taskNameList)

				except:
					print "[!]please Input the vaild taskname!"
				break

		elif parameter == 'status' and self.taskInfo:
			ShowTaskId()

		elif parameter == 'delete' and self.taskInfo:
			ShowTaskId()
			while True:
				try:
					taskName = raw_input("[+]Input taskname:")
					taskId = self.taskInfo[taskName]
					delUrl = baseUrl + '/task/%s/delete' % taskId
					if DelTask(delUrl):
						self.taskInfo.pop(taskName)

				except:
					print "[!]please Input the vaild taskname!"
				break

		elif parameter == 'data' and self.taskInfo:
			ShowTaskId()
			while True:
				try:
					taskName = raw_input("[+]Input taskname:")
					taskId = self.taskInfo[int(taskName)][0]
					taskStatus = self.taskInfo[int(taskName)][1]
					if taskStatus != "terminated":
						print "[!]please wait the scan compelete or start-up this task first!"
					else:
						dataUrl = baseUrl + '/scan/%s/data' % taskId
						GetData(dataUrl)

				except:
					print "[!]please Input the vaild taskname!"
				break

		elif parameter == 'stop' and self.taskInfo:
			ShowTaskId()
			while True:
				try:
					taskName = raw_input("[+]Input taskname:")
					taskId = self.taskInfo[taskName][0]
					taskStatus = self.taskInfo[taskName][1]
					if taskStatus == "not running" or taskStatus == 'terminated':
						print "[!]this task has been stoped!"
					else:
						stopUrl = baseUrl + '/scan/%s/stop' % taskId
						StopScan(stopUrl)

				except:
					print "[+]please Input the vaild taskname!"
				break

		elif parameter == 'exit':
			print "bye!"
			sys.exit(2)

		elif self.taskInfo:
			print "[!]please input the valid parameter!"

		else:
			print "[!]please create task first!"
if __name__=="__main__":
    main()
