#THIS IS A TEMPLATE SPIDER FOR WHAT WE CALL PHASE A
#ITEMS, LOGGING SYSTEM AND OUTPUT FILES WILL HAVE ALWAYS THE 
#SAME STRUCTURE AND BEHAVIOUR FOR EVERY SPIDER IN PHASE A


import datetime
import scrapy
from scrapy.http import Request, FormRequest
from twsc.items import *
import json
from scrapy.http import HtmlResponse


class PhaseASpider(scrapy.Spider):
	name = "nike"
	location_file = open('locations_nike.txt')
	handle_httpstatus_list = [500, 503, 403, 504, 400, 404, 408,502,429,550]
	#IMPORT LOGGING FOR OUR INTENAL LOGGING SISTEM
	
	#READING EXTERNAL FILE FOR LOCATIONS
	LOCATIONS = location_file.readlines()
	
	#STEP 1: READING FROM EXTERNAL FILES THE INPUT COUNTRIES WHERE THE CRAWLER MUST RUN. CREATE A FILE WHERE ALL THE COUNTRIES WHERE THE WEBSITE SHIPS TO.
	def start_requests(self):
		for line in self.LOCATIONS:
			url, country=line.split('|')
			yield Request(url, callback=self.test_url, meta={'country':country.strip()}, dont_filter=True)


	def test_url(self, response):
		response_data=json.loads(response.text)
		print(response_data['parsing'])
		try:
			#MULTIPLE OFFERS PAGE
			for product in response_data['parsing']['entities']['Product']:
				name=product['description']
				imageurl=product['image']
				for offer in product['offers']['offers']:
					sku=offer['itemOffered']['model']
					color=offer['itemOffered']['color']
					currency=offer['priceCurrency']
					price=offer['price']
					itemurl=offer['url']
					mpn=response.url[::-1].split('/')[0][::-1]
					item = PhaseAItem(
						sku=sku,
						color=color,
						price=price,
						currency=currency,
						country=response.meta.get('country'),
						itemurl=itemurl,
						imageurl=imageurl,
						name=name,
						mpn=mpn
					)
					yield item
		except:
			for product in response_data['parsing']['entities']['Product']:
				name=product['description']
				imageurl=product['image']
				try:
					sku=product['model']
				except:
					sku='n.a.'
				try:
					#exception for SAU
					mpn=product['mpn']
				except:
					mpn=response.url[::-1].split('/')[0][::-1]
				try:
					color=product['color']
				except:
					color='n.a.'
				currency=product['offers']['priceCurrency']
				price=product['offers']['price']
				itemurl=response.url
				item = PhaseAItem(
					sku=sku,
					color=color,
					price=price,
					currency=currency,
					country=response.meta.get('country'),
					itemurl=itemurl,
					imageurl=imageurl,
					name=name,
					mpn=mpn
				)
				yield item

			yield item
			