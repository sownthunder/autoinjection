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

	def __getnews_id(self,url):
		mm = url.split("&news_id")[0]
		return mm

	def __gettownName(self,url):
		mm = url.split("&townName")[0]
		return mm

	def request_seen(self,request):
		fp = self.__getid(request.url)
		catid = self.__getcatid(request.url)
		news_id = self.__getc(request.url)
		townName = self.__getm(request.url)
		if fp in self.fingerprints \
		or catid in self.fingerprints \
		or news_id in self.fingerprints \
		or townName in self.fingerprints \
		:
			return True
		self.fingerprints.add(fp)
		self.fingerprints.add(catid)
		self.fingerprints.add(news_id)
		self.fingerprints.add(townName)
