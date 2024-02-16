
from playwright.sync_api import sync_playwright
from scrapy.http import HtmlResponse
import json
import csv


with sync_playwright() as p:

	browser = p.chromium.launch(channel='chrome', headless=False,slow_mo=200)
	page = browser.new_page()
	page.goto('https://www.valentino.com/en-gb/', timeout=0)
	page.wait_for_load_state()
	html=HtmlResponse(url="my HTML string", body=page.content(), encoding='utf-8')
	
	categories = html.xpath('//a[@class="column-element"]/@href').extract()
	for cat in categories:
		print(cat)
		page.goto(cat, timeout=0)
		page.wait_for_load_state()
		html_plp=HtmlResponse(url="my HTML string", body=page.content(), encoding='utf-8')
		products = html_plp.xpath('//a[@class="productCard__image"]/@href').extract()
		for product in products:
			page.goto(product, timeout=0)
			page.wait_for_load_state()
			html_pdp=HtmlResponse(url="my HTML string", body=page.content(), encoding='utf-8')
			json_data_str= html_pdp.xpath('//script[contains(text(), "cif_productData")]/text()').extract()[0].split('cif_productData = "')[1].split('productData')[0].strip()[:-2].replace('\\x22', '"')
			json_data = json.loads(json_data_str)
			product_code = json_data['responseData']['sku']
			full_price = json_data['responseData']['price_range']['maximum_price']['regular_price']['value']
			price = json_data['responseData']['price_range']['maximum_price']['final_price']['value']
			currency_code = json_data['responseData']['price_range']['maximum_price']['final_price']['currency']
			product_category = json_data['responseData']['product_hierarchy'].split('/')[3]
			product_subcategory = json_data['responseData']['product_hierarchy'].split('/')[4]
			gender = json_data['responseData']['gender']
			itemurl = product
			image_url = json_data['responseData']['image']['responseData']['url'].replace('[image]', 'image').replace('[divArea]', '500x0')
			product_name = html_pdp.xpath('//h1[@class="productInfo__title"]/text()').extract()[0]
			with open("output.txt", "a") as file:
				csv_file = csv.writer(file, delimiter="|")
				csv_file.writerow([product_code,full_price,price,currency_code,product_category,product_subcategory,gender,itemurl,image_url, product_name])
			file.close()
		
	page.close()
	browser.close()

