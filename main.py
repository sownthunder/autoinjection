import requests
import re
import urlparse
import getopt
import json
import sys
import os
from sqlmap import modulePath
from lib.parse.cmdline import cmdLineParser
from lib.core.common import getUnicode
from lib.core.data import conf
from lib.core.data import newoptiondict

baseUrl = 'http://127.0.0.1:8775'
absDirectory = os.path.join(modulePath(),'txt\\urllist.txt')

def UpdateDict(optiondict):
	for key,value in optiondict.items():
		if value != None:
			newoptiondict[key] = value
	return newoptiondict

class autoinjection():
	def __init__(self):
		#self.taskInfo is a dictionary looks like {taskname:[taskId,taskStatus]}
		self.taskInfo = dict()
		self.taskidList = [] #self.GetTaskList()
		self.urlList = []

	def usage(self):
		print ""
		print "Options:"
		print "  help       get this usage information"
		print "  new        /task/new              build a new task"
		print "  scan       /scan/<taskid>         begin to scan target url"
		print "  delete     /task/<taskid>/delete  delete a scan task"
		print "  status     /scan/<taskid>/status  check the task status"
		print "  data       /scan/<taskid>/data    check the task result"
		print "  stop       /scan/<taskid>/stop    stop the task"
		print "  set        /option/<taskid>/set   set options"
		print "  list       /option/<taskid>/list  list all options of the task"

	def ShowTask(self):
		print " ------------ ------------------ ------------"
		print "|  taskname  |       taskid     |   status   |"
		print " ------------ ------------------ ------------"
		for taskname in self.taskInfo:
			print "|{:^11}".format(taskname),"|{:^17}".format(self.taskInfo[taskname][0]),"|{:^11}".format(self.taskInfo[taskname][1]),"|"
			print " ------------ ------------------ ------------"

	def AdminFlush(self):
		flushUrl = baseUrl + '/admin/a/flush'
		r = requests.get(flushUrl)
		#info = r.json()

	def SetOptions(self,setOptUrl,optiondict):
		r = requests.post(setOptUrl,data=json.dumps(optiondict),headers={'Content-Type':'application/json'})
		info = r.json()
		if info['success']:
			print ""
			print "[!]options have been set!"
			print ""
		else:
			print ""
			print "[!]set options failed!"
			print ""

	def ListOptions(self,listOptUrl):
		r = requests.get(listOptUrl)
		info = r.json()
		if info['success']:
			print ""
			for key in info['options']:
				print "%s => %s" % (key,info['options'][key])
			print ""
		else:
			print ""
			print "[!]get options list failed!"
			print ""

	def BuildTask(self):
		newUrl = baseUrl + "/task/new"
		#open urlList.txt and read urls
		f = open(absDirectory,'r')
		self.urlList = f.readlines()

		for n in range(0,len(self.urlList)):
			r = requests.get(newUrl)
			info = r.json()
			self.taskidList.append(info['taskid'])
			r.close()
		f.close()

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
				print "[!]task begin to run! targeturl: %s" % targetUrl
				print "[+]engineid: %s" % info["engineid"]
				print "[+]success: %s" % info["success"]
				print ""
				return 1
			else:
				print ""
				print "[!]task run failed!"
				print ""
				return 0

	def multiStart(self,taskNameList):
		for taskName in taskNameList:
			taskName.strip()
			beginTaskName = int(taskName.split('-')[0])
			endTaskName = int(taskName.split('-')[-1])
			while beginTaskName != endTaskName+1:
				taskId = self.taskInfo[beginTaskName][0]
				taskStatus = self.taskInfo[beginTaskName][1]
				if taskStatus == "running":
					print "[!]task %s has been started,please be patience." % (beginTaskName)
				else:
					scanUrl = baseUrl + '/scan/%s/start' % taskId
					if self.BeginScan(scanUrl,self.urlList[0].rstrip('\n')):
						self.urlList.pop(0)

				beginTaskName += 1

	def multiDelete(self,taskNameList):
		for taskName in taskNameList:
			taskName.strip()
			beginTaskName = int(taskName.split('-')[0])
			endTaskName = int(taskName.split('-')[-1])
			while beginTaskName != endTaskName+1:
				taskId = self.taskInfo[beginTaskName][0]
				delUrl = baseUrl + '/task/%s/delete' % taskId
				if self.DelTask(delUrl):
					self.taskidList.remove(taskId)
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
					print "[+]error: %s" % info["error"]
					print ""
			elif not info["data"]:
				print ""
				print "[!]this site are unvunlerable or you can restart it!"
				print ""
			else:
				print ""
				print "[!]Injection failed!"
				print "[+]message: %s" % info["message"]
				print ""
		except:
			print "[!]please run task before check the result!"

	def GetTaskList(self):
		listUrl = 'http://127.0.0.1:8775/admin/a/list'
		r = requests.get(listUrl)
		info = r.json()
		taskname = 1
		for taskid,taskstatus in info['tasks'].items():
			self.taskInfo[taskname] = [taskid,taskstatus]
			taskname += 1

def main():
	autoSqli = autoinjection()
	autoSqli.usage()

	while True:
		try:
			parameter = raw_input("[+]Input command:")
		except:
			sys.exit(0)
		if parameter == 'help':
			autoSqli.usage()

		elif parameter == 'new':
			autoSqli.AdminFlush()
			autoSqli.BuildTask()
			autoSqli.GetTaskList()

		elif parameter == 'scan' and autoSqli.taskInfo:
			autoSqli.ShowTask()
			try:
				taskNameString = raw_input("[+]Input taskname:")
				if taskNameString == 'all':
					taskNameString = '1-%d' % (len(autoSqli.taskidList))
				taskNameList = taskNameString.split(",")
				autoSqli.multiStart(taskNameList)
			except:
				print "[!]please Input the vaild taskname!"
			autoSqli.GetTaskList()

		elif parameter == 'status' and autoSqli.taskInfo:
			autoSqli.GetTaskList()
			autoSqli.ShowTask()

		elif parameter == 'delete' and autoSqli.taskInfo:
			autoSqli.ShowTask()
			try:
				taskName = raw_input("[+]Input taskname:")
				taskNameList = taskNameString.split(",")
				autoSqli.multiDelete(taskNameList)
			except:
				print "[!]please Input the vaild taskname!"
			autoSqli.GetTaskList()

		elif parameter == 'data' and autoSqli.taskInfo:
			autoSqli.GetTaskList()
			autoSqli.ShowTask()
			try:
				taskName = raw_input("[+]Input taskname:")
				taskId = autoSqli.taskInfo[int(taskName)][0]
				taskStatus = autoSqli.taskInfo[int(taskName)][1]
				if taskStatus != "terminated":
					print "[!]please wait the scan compelete or start-up this task first!"
				else:
					dataUrl = baseUrl + '/scan/%s/data' % taskId
					autoSqli.GetData(dataUrl)
			except:
				print "[!]please Input the vaild taskname!"

		elif parameter == 'set' and autoSqli.taskInfo:
			autoSqli.ShowTask()
			try:
				taskName = raw_input("[+]Input taskname:")
				taskOption = raw_input("[+]Input option(same as sqlmap command line):")
				OptionList = taskOption.split(" ")
				optiondict = UpdateDict(cmdLineParser(OptionList).__dict__)
				conf.update(optiondict)
				taskId = autoSqli.taskInfo[int(taskName)][0]
				setOptUrl = baseUrl + '/option/%s/set' % taskId
				autoSqli.SetOptions(setOptUrl,conf)
			except:
				print "[+]please Input the vaild taskname!"
			autoSqli.GetTaskList()

		elif parameter == 'list' and autoSqli.taskInfo:
			autoSqli.ShowTask()
			try:
				taskName = raw_input("[+]Input taskname:")
				taskId = autoSqli.taskInfo[int(taskName)][0]
				listOptUrl = baseUrl + '/option/%s/list' % taskId
				autoSqli.ListOptions(listOptUrl)
			except:
				print "[+]please Input the vaild taskname!"
			autoSqli.GetTaskList()

		elif parameter == 'stop' and autoSqli.taskInfo:
			#autoSqli.GetTaskList()
			autoSqli.ShowTask()
			try:
				taskName = raw_input("[+]Input taskname:")
				taskId = autoSqli.taskInfo[taskName][0]
				taskStatus = autoSqli.taskInfo[taskName][1]
				if taskStatus == "not running" or taskStatus == 'terminated':
					print "[!]this task has been stoped!"
				else:
					stopUrl = baseUrl + '/scan/%s/stop' % taskId
					autoSqli.StopScan(stopUrl)
			except:
				print "[+]please Input the vaild taskname!"
			autoSqli.GetTaskList()

		elif parameter == 'exit':
			print "bye!"
			sys.exit(0)

		elif autoSqli.taskInfo:
			print "[!]please input the valid parameter!"

		else:
			print "[!]please create task first!"

if __name__=="__main__":
	main()
