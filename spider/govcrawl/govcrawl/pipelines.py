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
		mm = url.split("&id")[0]
		return mm

	def __getcatid(self,url):
		mm = url.split("&catid")[0]
		return mm

	def __getc(self,url):
		mm = url.split("&c")[0]
		return mm

	def __getrssid(self,url):
		mm = url.split("&rssid")[0]
		return mm

	def __geta(self,url):
		mm = url.split("&a")[0]
		return mm

	def __getm(self,url):
		mm = url.split("&m")[0]
		return mm

	def process_item(self, item, spider):
		rssid = self.__getrssid(item['link'])
		fp = self.__getid(item["link"])
		catid = self.__getcatid(item["link"])
		a = self.__geta(item["link"])
		#m = self.__getm(request.url)
		if fp in self.seen \
		or catid in self.seen \
		or a in self.seen \
		or rssid in self.seen \
		:
			raise DropItem('Duplicate link %s' % item['link'])
		self.seen.add(fp)
		self.seen.add(catid)
		self.seen.add(a)
		self.seen.add(rssid)

		line = item["link"]+'\n'
		self.file.write(line)
		return item
