# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ValentinoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
	product_code = scrapy.Field()
	full_price = scrapy.Field()
	price = scrapy.Field()
	currency_code = scrapy.Field()
	country_code = scrapy.Field()
	item_URL = scrapy.Field()
	image_URL = scrapy.Field()
	product_name = scrapy.Field()
	gender = scrapy.Field()
	product_category = scrapy.Field()
	product_subcategory = scrapy.Field()
    pass
