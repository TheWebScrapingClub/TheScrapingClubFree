# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LoeweItem(scrapy.Item):
    Productcode = scrapy.Field()
    Gender = scrapy.Field()
    Fullprice = scrapy.Field()
    Price = scrapy.Field()
    Currency = scrapy.Field()
    country = scrapy.Field()
    itemurl = scrapy.Field()
    brand = scrapy.Field()
    website = scrapy.Field()
    data = scrapy.Field()
    pricemax = scrapy.Field()