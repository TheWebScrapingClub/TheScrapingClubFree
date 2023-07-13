
import datetime
import scrapy
from scrapy.http import Request, FormRequest
from twsc.items import *


class PhaseASpider(scrapy.Spider):
	name = "tests"
	location_file = open('locations.txt')
	handle_httpstatus_list = [500, 503, 403, 504, 400, 404, 408,502,429,550]
	
	LOCATIONS = location_file.readlines()
	
	def start_requests(self):
		for line in self.LOCATIONS:
			url, website, antibot = line.split('|')
			yield Request(url, callback=self.test_url, meta={'website':website, 'antibot':antibot.strip()}, headers={'X-SU-Headless': 'html'}, dont_filter=True)


	def test_url(self, response):
		try:
			try:
				test_content=response.xpath('//meta[@property="og:title"]/@content').extract()[0]
			except:
				test_content=response.xpath('//title/text()').extract()[0]
		except:
			#print(response.text)
			test_content='N.A.'
		item = PhaseAItem(
			itemurl=response.url,
			status=response.status,
			antibot=response.meta.get('antibot'),
			website=response.meta.get('website'),
			test_content=test_content.strip()
		)
		yield item
