# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class LuisaviaromaItem(Item):
    productcode = Field()
    gender = Field()
    fullprice = Field()
    price = Field()
    currency = Field()
    country = Field()
    itemurl = Field()
    brand = Field()
    website = Field()
    competence_date = Field()
    pricemax = Field()