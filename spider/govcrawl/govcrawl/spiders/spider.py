import scrapy
from tutorial.items import TutorialItem
import re

class GovSpider(scrapy.Spider):
	name = "chengwill"

	allowed_domains = ["chengwill.cn"]
	start_urls = ["http://www.chengwill.cn/blog"]
	def parse(self,response):
		sel = scrapy.Selector(response)
		article_info = sel.xpath("//a")

		for info in article_info:
			item = TutorialItem()
			link = info.xpath('@href').extract()
			position = link[0].find("/")
			if position < 0:
				continue
			elif "http" not in link[0]:
				url = response.url + link[0][position:]
			elif re.match(r'http://www\.chengwill\.cn/.*',link[0]):
				url = link[0]
			else:
				continue
			yield scrapy.Request(url,callback=self.parse)
			item['link'] = url
			title = info.xpath('text()').extract()
			if title:
				item['title'] = title[0]
			else:
				item['title'] = None
			print item['title'],item['link']
			#raw_input("stop!")
			yield item
