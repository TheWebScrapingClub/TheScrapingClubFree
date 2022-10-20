# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookstoscrapeItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	title = scrapy.Field()
	imageurl = scrapy.Field()
	upc = scrapy.Field()
	producttype = scrapy.Field()
	pricenotax = scrapy.Field()
	pricewithtax = scrapy.Field()
	availability = scrapy.Field()
	reviewsnum = scrapy.Field()
	description = scrapy.Field()
	pass
