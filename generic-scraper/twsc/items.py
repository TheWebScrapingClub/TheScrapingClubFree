# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field


import scrapy


class EcommerceItem(scrapy.Item):
    productcode = scrapy.Field()
    fullprice = scrapy.Field()
    price = scrapy.Field()
    currency=scrapy.Field()
    category = scrapy.Field()
    imageurl = scrapy.Field()
    itemurl = scrapy.Field()
    brand = scrapy.Field()
    productname = scrapy.Field()
    website = scrapy.Field()
