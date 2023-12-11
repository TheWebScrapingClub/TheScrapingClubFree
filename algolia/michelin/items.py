# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class restaurantItem(scrapy.Item):
	# define the fields for your item here like:
	res_id=scrapy.Field()
	name = scrapy.Field()
	chef = scrapy.Field()
	stars = scrapy.Field()
	cuisine_code = scrapy.Field()
	price_category = scrapy.Field()
	country = scrapy.Field()
	region = scrapy.Field()
	city = scrapy.Field()
	lat  = scrapy.Field()
	lon  = scrapy.Field()
	json_data = scrapy.Field()
	pass
