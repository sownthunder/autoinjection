import requests
import urlparse
import getopt
import json
import sys
import os

def GetTaskId(newUrl):
    r = requests.get(newUrl)
    info = r.json()
    taskid = info["taskid"]
    r.close()
    return taskid

baseUrl = 'http://127.0.0.1:8775'
taskInfo = dict()
taskInfo["1"]="afdafd"
status = "not running"
#server = os.popen(r'server.py')

def usage():
    print ""
    print "Options:"
    print "  new        /task/new              build a new task"
    print "  scan       /scan/<taskid>         begin to scan target url"
    print "  delete     /task/<taskid>/delete  delete a scan task"
    print "  status     /scan/<taskid>/status  check the task status"
    print "  data       /scan/<taskid>/data    check the task result"

def ShowTaskId():
    print " ------------ ------------------ ------------"
    print "|  taskname  |       taskid     |   status   |"
    print " ------------ ------------------ ------------"
    for task in taskInfo:
        print "|{:^11}".format(task),"|%-*s"%(17,taskInfo[task]),"|%-*s"%(10,status),"|"
        print " ------------ ------------------ ------------"

def main():
    usage()
    newUrl = ''
    scanUrl = ''
    delUrl = ''
    staUrl = ''
    dataUrl = ''
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
                taskid = GetTaskId(newUrl)
                taskInfo["task%s"%tasknumber] = taskid
                tasknumber = tasknumber + 1
        elif parameter == 'scan' and taskInfo:
            ShowTaskId()
            while True:
                try:
                    taskName = raw_input("[+]Input taskname:")
                    taskId = taskInfo[taskName]
                    scanUrl = baseUrl + '/scan/%s/start' % taskId
                    if BeginScan(scanUrl,urlList[0]):
                        urlList.pop(0)
                        break
                except:
                    print "[!]please Input the vaild taskname!"

        elif parameter == 'delete' and taskInfo:
            ShowTaskId()
            while True:
                try:
                    taskName = raw_input("[+]Input taskname:")
                    taskId = taskInfo[taskName]
                    delUrl = baseUrl + '/task/%s/delete' % taskId
                    if DelTask(delUrl):
                        taskInfo.pop(taskName)
                        break
                except:
                    print "[!]please Input the vaild taskname!"
        elif parameter == 'status' and taskInfo:
            ShowTaskId()
            while True:
                try:
                    taskName = raw_input("[+]Input taskname:")
                    taskId = taskInfo[taskName]
                    staUrl = baseUrl + '/scan/%s/status' % taskId
                    GetStatus(staUrl)
                    break
                except:
                    print "[!]please Input the vaild taskname!"

        elif parameter == 'data' and taskInfo:
            ShowTaskId()
            while True:
                try:
                    taskName = raw_input("[+]Input taskname:")
                    taskId = taskInfo[taskName]
                    dataUrl = baseUrl + '/scan/%s/data' % taskId
                    GetData(dataUrl)
                    break
                except:
                    print "[!]please Input the vaild taskname!"
        elif taskInfo:
            print "[!]please input the valid parameter!"
        else:
            print "[!]please create task first!"

    #BeginScan(scanUrl)
if __name__=="__main__":
    ShowTaskId()
    #main()
