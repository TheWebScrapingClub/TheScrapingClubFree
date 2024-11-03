import datetime
import scrapy
from twsc.items import *
import requests
from base64 import b64decode 
from scrapy.http import Request, FormRequest
import time





class PhaseASpider(scrapy.Spider):
	name = "generic_scraper"
	NOT_FOUND='N.A.'
	def start_requests(self):
		location_file = open('locations.txt')
		handle_httpstatus_list = [500, 503, 403, 504, 400, 404, 408,502,429,550,520]
		
		#READING EXTERNAL FILE FOR LOCATIONS
		LOCATIONS = location_file.readlines()
		for line in LOCATIONS:
			url, website = line.split('|')
			yield Request(
				url, callback=self.parse_navigation, 
				meta={
					"zyte_api_automap": {
						"productNavigation": True 
					},
					"website": website.strip(), 
					"index": 0
				},
			)

	def parse_navigation(self, response):
		limit = 10
		index = response.meta.get('index')
		productNavigation = response.raw_api_response["productNavigation"]
		print(productNavigation)
		for item in productNavigation["items"]:
			yield Request(item['url'], callback=self.parse_item, 
					meta={
						"zyte_api_automap": {
						"product": True 
						},
					"website": response.meta.get('website')
					})
		if index < limit:
			try:
				next_page = productNavigation["nextPage"]['url']
				index += 1
				yield Request(next_page, callback=self.parse_navigation, meta={
					"zyte_api_automap": {
						"productNavigation": True 
					},
					"website": response.meta.get('website'), 
					"index": index
				},)
			
			except:
				print("No next page")
				pass
		else:
			print("Limit reached")


	def parse_item(self, response):
		print(response)
		product_data=response.raw_api_response["product"]
		try:
			productcode=product_data['sku']
		except:
			productcode=self.NOT_FOUND
		try:
			fullprice=product_data['regularPrice']
		except:
			fullprice=self.NOT_FOUND
		try:
			price=product_data['price']
		except:
			price=self.NOT_FOUND
		try:
			currency=product_data['currency']
		except:
			currency=self.NOT_FOUND
		try:
			category=product_data['breadcrumbs']
		except:
			category=self.NOT_FOUND
		try:
			imageurl=product_data['mainImage']['url']
		except:
			imageurl=self.NOT_FOUND
		try:
			productname=product_data['name']
		except:
			productname=self.NOT_FOUND
		try:
			brand=product_data['brand']['name']
		except:
			brand=self.NOT_FOUND
		item = EcommerceItem(
			productcode=productcode,
			fullprice=fullprice,
			price=price,
			currency=currency,
			category=category,
			brand=brand,
			imageurl=imageurl, 
			productname=productname,
			itemurl=response.url,
			website=response.meta.get('website'),
		)
		yield item