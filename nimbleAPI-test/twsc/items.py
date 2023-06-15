# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field


import scrapy


class PhaseAItem(scrapy.Item):
	sku=scrapy.Field()
	color=scrapy.Field()
	price=scrapy.Field()
	currency=scrapy.Field()
	country=scrapy.Field()
	itemurl=scrapy.Field()
	imageurl=scrapy.Field()
	name=scrapy.Field()
	mpn=scrapy.Field()
