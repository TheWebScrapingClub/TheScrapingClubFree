from botasaurus import *
from lxml import etree 
import json
import time
from random import randrange

@request(use_stealth=True)
def scrape_heading_task(request: AntiDetectRequests, data):
	soup = request.bs4("https://www.harrods.com/")
	interval=randrange(10)
	time.sleep(interval)
	category = request.bs4("https://www.harrods.com/en-it/shopping/women-clothing-dresses")
	    # Retrieve the heading element's text
	dom = etree.HTML(str(category)) 
	json_data=json.loads(dom.xpath('//script[contains(text(), "ItemList")]/text()')[0])
	for url_list in json_data['itemListElement']:
		url='https://www.harrods.com'+url_list['url'].replace('/shopping/shopping', '/shopping')
		print(url)
		product_page=request.get(url)
		print(product_page.status_code)
		dom_page = etree.HTML(product_page.text)
		price=dom_page.xpath('//span[@data-test="product-price"]/text()')[0]
		print(price)
		interval=randrange(10)
		time.sleep(interval)

scrape_heading_task()
