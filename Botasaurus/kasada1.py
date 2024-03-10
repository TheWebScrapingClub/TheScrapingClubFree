from botasaurus import *
from lxml import etree 
import json
import time
from random import randrange

@request(use_stealth=True)
def scrape_heading_task(request: AntiDetectRequests, data):
	soup = request.bs4("https://www.canadagoose.com/us/en/")
	interval=randrange(10)
	time.sleep(interval)
	category = request.bs4("https://www.canadagoose.com/us/en/shop/women/outerwear/parkas/")
	    # Retrieve the heading element's text
	dom = etree.HTML(str(category)) 
	url_list=dom.xpath('//a[@itemprop="url"]/@href')
	for url in url_list:
		final_url='https://www.canadagoose.com'+url
		print(url)
		product_page=request.get(url)
		print(product_page.status_code)
		dom_page = etree.HTML(product_page.text)
		price=dom_page.xpath('//h4[@itemprop="name"]/text()')[0]
		print(price)
		interval=randrange(10)
		time.sleep(interval)

scrape_heading_task()
