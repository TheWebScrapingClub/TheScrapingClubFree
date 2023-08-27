import scrapy
from scrapy.http import Request
import json
import csv
import nopecha

class BooksscraperSpider(scrapy.Spider):
	name = 'capchasolving'
	
	# READING EXTERNAL FILE FOR LOCATIONS
	
	def start_requests(self):
		yield Request('https://nopecha.com/demo/recaptcha#easy', callback=self.solve_captcha)
			
	def solve_captcha(self, response):
		#sitekey=response.xpath('//div/@data-sitekey').extract()[0]
		nopecha.api_key = ''

		# Call the Token API
		token = nopecha.Token.solve(
		    type='recaptcha2',
		    sitekey='6Ld8NA8jAAAAAPJ_ahIPVIMc0C4q58rntFkopFiA',
		    url='https://nopecha.com/demo/recaptcha#easy',
		    data={
		        'action': 'check',
		    }
		)

		# Print the token
		print(token)
		
