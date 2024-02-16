"""
Scrapy item models module

This module defines Scrapy item models for scraped data. Items represent structured data
extracted by spiders.

For detailed information on creating and utilizing items, refer to the official documentation:
https://docs.scrapy.org/en/latest/topics/items.html
"""

from scrapy import Field, Item


class GucciItem(Item):

	website_name = Field()
	competence_date = Field()
	brand = Field()
	product_code = Field()
	country_code = Field()
	currency_code = Field()
	full_price = Field()
	price = Field()
	category1_code = Field()
	category2_code = Field()
	category3_code = Field()
	title = Field()
	imageurl = Field()
	itemurl = Field()

