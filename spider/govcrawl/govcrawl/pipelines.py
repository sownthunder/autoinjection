# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.exceptions import DropItem
import urlparse

class GovcrawlPipeline(object):
	def __init__(self):
		self.file = open("..\\..\\txt\\urllist.txt","w")
		f = open("..\\..\\txt\\value.txt",'r')
		self.valuedict = f.readlines()
		self.seen = set()

	def __getValue(self,url):
		for value in self.valuedict:
			div_by_value = url.split(value.rstrip('\n'))
			mm = div_by_value[0]
			if mm in self.seen:
				raise DropItem('Duplicate link %s' % url)
			elif len(div_by_value) > 1:
				self.seen.add(mm)
				line = url+'\n'
				print url
				self.file.write(line)

	def process_item(self, item, spider):
		self.__getValue(item['link'])
		#self.file.close()
		return item
