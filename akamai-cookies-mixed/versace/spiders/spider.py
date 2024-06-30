# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from versace.items import *
from datetime import datetime
from scrapy.selector import Selector
import re
import ast
import json
import csv

class LoeweSpider(scrapy.Spider):
	name = "radar"

	location_file = open('locations.txt')
	DEFAULT_VALUE="n.a."

	LOCATIONS = location_file.readlines()
	def start_requests(self):
		for i, url in enumerate(self.LOCATIONS):
			yield Request(url,  callback=self.parse_home_page, dont_filter=True)
	
	def parse_home_page(self, response):
		macro_categories=response.xpath('//h2[@role="menuitem"]/a/@href').extract()
		for cat in macro_categories:
			print(cat)
			yield Request(cat,  callback=self.parse_cat_page, dont_filter=True)
		
		
		
	def parse_cat_page(self, response):
		products=response.xpath('//h2[@class="link back-to-product-anchor-js"]/a/@href').extract()
		for prod in products:
			yield Request(prod, callback=self.parse_product_page, meta=response.meta)
		
		try:
			next_page=response.xpath('//link[@rel="next" ]/@href').extract()[0]
			yield Request(next_page,  callback=self.parse_cat_page, dont_filter=True)
		except:
			pass
	
	def parse_product_page(self, response):
		
		title=response.xpath('//title/text()').extract()[0].strip()
	
		with open("output.txt", "a") as file:
			csv_file = csv.writer(file, delimiter="|")
			csv_file.writerow([title])
		file.close()
