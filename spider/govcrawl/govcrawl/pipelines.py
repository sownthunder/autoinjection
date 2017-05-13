# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.exceptions import DropItem

class GovcrawlPipeline(object):
	def __init__(self):
		self.file = open("..\\..\\txt\\urllist.txt","w")
		self.seen = set()

	def __getid(self,url):
		mm = url.split("id")[0]
		return mm

	def __getcatid(self,url):
		mm = url.split("catid")[0]
		return mm

	def __getc(self,url):
		mm = url.split("&c")[0]
		return mm

	def __getrssid(self,url):
		mm = url.split("rssid")[0]
		return mm

	def __geta(self,url):
		mm = url.split("&a")[0]
		return mm

	def __getID(self,url):
		mm = url.split("ID")[0]
		return mm
		
	def __getdeptName(self,url):
		mm = url.split("deptName")[0]
		return mm
		
	def __getcid(self,url):
		mm = url.split("cid")[0]
		return mm
		
	def __getnews_id(self,url):
		mm = url.split("news_id")[0]
		return mm
		
	def __getsub_id(self,url):
		mm = url.split("sub_id")[0]
		return mm
		
	def __getsubId(self,url):
		mm = url.split("subId")[0]
		return mm
		
	def __getsurveyId(self,url):
		mm = url.split("surveyId")[0]
		return mm
		
	def __gettypeid(self,url):
		mm = url.split("typeid")[0]
		return mm

	def process_item(self, item, spider):
		rssid = self.__getrssid(item['link'])
		fp = self.__getid(item["link"])
		catid = self.__getcatid(item["link"])
		a = self.__geta(item["link"])
		deptName = self.__getdeptName(item["link"])
		cid = self.__getcid(item["link"])
		news_id = self.__getnews_id(item["link"])
		sub_id = self.__getsub_id(item["link"])
		subId = self.__getsubId(item["link"])
		surveyId = self.__getsurveyId(item["link"])
		typeid = self.__gettypeid(item["link"])
		ID = self.__getID(item["link"])
		if fp in self.seen \
		or catid in self.seen \
		or a in self.seen \
		or rssid in self.seen \
		or deptName in self.seen \
		or cid in self.seen \
		or news_id in self.seen \
		or sub_id in self.seen \
		or subId in self.seen \
		or surveyId in self.seen \
		or typeid in self.seen \
		or ID in self.seen \
		:
			raise DropItem('Duplicate link %s' % item['link'])
		self.seen.add(fp)
		self.seen.add(catid)
		self.seen.add(a)
		self.seen.add(rssid)
		self.seen.add(deptName)
		self.seen.add(cid)
		self.seen.add(news_id)
		self.seen.add(sub_id)
		self.seen.add(subId)
		self.seen.add(surveyId)
		self.seen.add(typeid)
		self.seen.add(ID)

		line = item["link"]+'\n'
		self.file.write(line)
		#self.file.close()
		return item
