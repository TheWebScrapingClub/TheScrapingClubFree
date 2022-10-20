import scrapy
from scrapy.http import Request
import json
import csv

class BooksscraperSpider(scrapy.Spider):
	name = 'kallax'
	
	input_file = open("inputlist.txt")
	# READING EXTERNAL FILE FOR LOCATIONS
	LOCATIONS = input_file.readlines()
	PRODUCT_CODES = ['20275814', '70351886']
	
	def start_requests(self):
		for product_code in self.PRODUCT_CODES:
			for line in self.LOCATIONS:
				country, locale = line.split('|')
				url = 'https://sik.search.blue.cdtapps.com/'+country+'/'+locale.strip()+'/search-result-page?max-num-filters=8&q='+product_code
				yield Request(url, callback=self.parse_json, meta={'country':country})
			
	def parse_json(self, response):
		data=json.loads(response.text)
		country=response.meta.get('country')
		try:
			#when product code is found
			for item in data['searchResultPage']['products']['main']['items']:
				price=item['product']['salesPrice']['numeral']
				currency=item['product']['salesPrice']['currencyCode']
				productid=item['product']['itemNo']
				with open("output.txt", "a") as file:
					csv_file = csv.writer(file, delimiter="|")
					csv_file.writerow([country, productid, price, currency])
				file.close()
		except:
			pass