import os
from scrapy.dupefilter import RFPDupeFilter
from scrapy.utils.request import request_fingerprint

class CustomFilter(RFPDupeFilter):
	'''def __init__(self,path='result.json',debug=False):
		#self.file = open("result.json","w")
		RFPDupeFilter.__init__(self,path,debug)'''

	def __getid(self,url):
		mm = url.split("&id")[0]
		return mm

	def __getcatid(self,url):
		mm = url.split("&catid")[0]
		return mm

	def __getc(self,url):
		mm = url.split("&c")[0]
		return mm

	def __getm(self,url):
		mm = url.split("&m")[0]
		return mm

	def request_seen(self,request):
		fp = self.__getid(request.url)
		catid = self.__getcatid(request.url)
		c = self.__getc(request.url)
		#m = self.__getm(request.url)
		if fp in self.fingerprints \
		or catid in self.fingerprints \
		or c in self.fingerprints \
		:
			return True
		self.fingerprints.add(fp)
		self.fingerprints.add(catid)
		self.fingerprints.add(c)
		#self.fingerprints.add(m)
		if self.file:
			self.file.write(request.url + os.linesep)
