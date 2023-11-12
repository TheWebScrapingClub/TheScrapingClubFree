import re, ast  
import datetime
from scrapy import Request, Spider
from luisaviaroma.items import LuisaviaromaItem
import json
import time
import hrequests
from scrapy.http import HtmlResponse


class RadarSpider(Spider):
	name = "radar"
	allowed_domains = ["luisaviaroma.com"]
	start_urls = (
		'http://www.google.com/',
	)
	locations_file = open('locations.txt')

	COUNTRIES = locations_file.readlines()

	def start_requests(self):
		for i, countrycurrency in enumerate(self.COUNTRIES):
			language, country, country_code, currency,category=countrycurrency.split(',')
			yield Request('https://www.google.com', callback=self.call_api, meta={'current_page':1, 'language':language, 'country':country,'country_code':country_code, 'currency':currency,'category':category.strip() }, dont_filter=True)
		
	def call_api(self, response):
		language = response.meta.get('language')
		country = response.meta.get('country')
		currency = response.meta.get('currency')
		category = response.meta.get('category')
		country_code=response.meta.get('country_code')
		total_pages=2
		current_page=response.meta.get('current_page')
		session=hrequests.BrowserSession(proxy_ip="YOURPROXYPROVIDER", headless=False)  
		url='https://www.luisaviaroma.com/'		
		akamai_test=session.get(url)
		page = akamai_test.render(mock_human=True)
		while current_page<total_pages:
			try:
				url='https://www.luisaviaroma.com/'+language+'-'+country+'/shop/'+category+'&Page='+str(current_page)+'&ajax=true'
				akamai_test=session.get(url)
				print(akamai_test.text)
				json_data=json.loads(akamai_test.text)
				website='LUISAVIAROMA'
				print(json_data)
				products = json_data["Items"]
				for product in products:
					item = LuisaviaromaItem()
					item['productcode'] = product["ItemCode"]
					item['gender'] = json_data['ContextInfo']['GenderMemo']
					item['fullprice'] = product["ListPrice"]
					item['price'] = product["ListPriceDiscounted"]
					item['currency'] = product["OfferMetaInfo"]['Currency']
					item['country'] = response.meta.get('country_code')
					item['itemurl'] = 'https://www.luisaviaroma.com/'+product["Url"]
					item['brand'] = product["Designer"]
					item['website'] = 'LUISAVIAROMA'
					item['competence_date'] = datetime.datetime.today().strftime('%Y%m%d')
					item['pricemax'] = 0
					yield item
		
				total_pages=json_data["Pagination"]["TotalePages"]
				current_page=json_data["Pagination"]["CurrentPage"]
				if current_page<total_pages:
					current_page=current_page+1
			except:
				url='https://www.luisaviaroma.com/'		
				akamai_test=session.get(url)
				page = akamai_test.render(mock_human=True)
			
			
	
		

