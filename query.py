import time
import requests

valueSet = set()

while True:
	staUrl = "http://127.0.0.1:8775/admin/a/list"
	r = requests.get(staUrl)
	info = r.json()
	for taskid,taskstatus in info['tasks']:
		if taskstatus == 'terminated' and taskid not in valueSet:
			valueSet.add(taskid)
			response = requests.get("http://127.0.0.1:8775/scan/%s/data" % taskid)
			datainfo = response.json()
			print

	if len(valueSet) == info['tasks_num']:
		break
	time.sleep(3)
