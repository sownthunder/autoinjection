import scrapy
from govcrawl.items import GovcrawlItem
import re
import urlparse

class GovSpider(scrapy.Spider):
	name = "govspider"
	download_delay = 1
	#allowed_domains = ['192.168.0.102']
	f = open("..\\..\\website.txt","r")
	websites = f.readlines()
	start_urls = ['%s' % (target.rstrip()) for target in websites]
	allowed_domains = ["%s" % (urlparse.urlparse(target.rstrip()).netloc) for target in websites]

	def parse(self,response):
		sel = scrapy.Selector(response)
		article_info = sel.xpath("//a")

		for info in article_info:
			item = GovcrawlItem()
			link = info.xpath('@href').extract()
			if not link:
				continue
			position = link[0].find("/")
			if position < 0 or "?" not in link[0]:
				continue
			elif "http" not in link[0]:
				url = response.url + link[0][position:]
			else:
				url = link[0]
			yield scrapy.Request(url,callback=self.parse)
			item['link'] = url
			title = info.xpath('text()').extract()
			if title:
				item['title'] = title[0]
			else:
				item['title'] = None
			print item['link']
			yield item
