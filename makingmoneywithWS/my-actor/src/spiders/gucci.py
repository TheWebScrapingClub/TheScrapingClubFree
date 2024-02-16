from __future__ import annotations

from typing import Generator
from urllib.parse import urljoin

from scrapy import Request, Spider
from scrapy.responsetypes import Response

from ..items import GucciItem


class GucciSpider(Spider):
	"""
	Scrapes title pages and enqueues all links found on the page.
	"""

	name = 'gucci_spider'

	# The `start_urls` specified in this class will be merged with the `start_urls` value from your Actor input
	# when the project is executed using Apify.
	start_urls = ['https://www.gucci.com/it/it/']

	def parse(self, response: Response) -> Generator[GucciItem | Request, None, None]:
		CODES = ["women", "men", "children", "jewelry-watches", "beauty", "decor"]
		for category_code in CODES:
			api_url = (
				'https://www.gucci.com/it/it/'
				+ "c/productgrid?categoryCode="
				+ category_code
				+ "&page=0"
			)
			#print(api_url)
			yield Request(api_url, callback=self.parse_json, meta=response.meta)

	def parse_json(self, response: Response) -> Generator[GucciItem | Request, None, None]:
		try:
			json_data = json.loads(response.body.decode("utf-8"))
			if json_data.get("products"):
				if json_data["products"].get("items"):
					products = json_data["products"]["items"]
					for product in products:
						product_code = product.get("productCode")
						itemurl = response.url.split("/c/")[0] + product.get("productLink")
						fullprice = (
							product.get("fullPrice") if product.get("fullPrice") else "0"
						)
						price = product.get("price") if product.get("price") else "0"
						if "/women/" in itemurl:
							gender = "Women"
						elif "/men/" in itemurl:
							gender = "Men"
						else:
							gender = "N.A"
						currency = (
							re.sub("\d?,?\.?\s?", "", price).strip() if price else "N.A"
						)
						brand = "GUCCI"
						website = "GUCCI"
						data = (datetime.now()).strftime("%Y%m%d")
						pricemax = "0"

						try:
							gender=product['categoryPath'].split('/')[0]
						except:
							gender=self.DEFAULT_VALUE
						try:
							category1_code=product['categoryPath'].split('/')[1]
						except:
							category1_code=self.DEFAULT_VALUE

						try:
							category2_code=product['categoryPath'].split('/')[2]
						except:
							category2_code=self.DEFAULT_VALUE

						try:
							category3_code=product['categoryPath'].split('/')[3]
						except:
							category3_code=self.DEFAULT_VALUE
						try:
							imageurl='http:'+product['primaryImage']['datasrcstandard']
						except:
							imageurl=self.DEFAULT_VALUE

						try:
							title=product['productName']
						except:
							title=self.DEFAULT_VALUE

						item = GucciItem(
							website_name = website,
							competence_date = data,
							brand = brand,
							product_code = product_code,
							country_code = 'ITA',
							currency_code = 'EUR',
							full_price = fullprice,
							price = price,
							category1_code = category1_code,
							category2_code = category2_code,
							category3_code = category3_code,
							title = title,
							imageurl = imageurl,
							itemurl = itemurl
						)
						yield item
					next_page_url = (
						response.url.split("&page=")[0]
						+ "&page="
						+ str(int(response.url.split("&page=")[1]) + 1)
					)
					yield Request(
						next_page_url,
						callback=self.parse_json,
						meta=response.meta,
						dont_filter=True,
					)
					
		except:
			pass


