# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field


import scrapy


class PhaseAItem(scrapy.Item):
    itemurl = scrapy.Field()
    status = scrapy.Field()
    antibot = scrapy.Field()
    website = scrapy.Field()
    test_content = scrapy.Field()
