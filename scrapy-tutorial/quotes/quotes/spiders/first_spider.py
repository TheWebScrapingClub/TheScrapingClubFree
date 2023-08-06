import scrapy
from quotes.items import *
from scrapy.http import Request

class FirstSpiderSpider(scrapy.Spider):
	name = 'first_spider'
	allowed_domains = ['toscrape.com']
	start_urls = ['https://quotes.toscrape.com/']

	def parse(self, response):
		quote_list = response.xpath('//div[@class="quote"]')
		for single_quote in quote_list:
			quote= single_quote.xpath('.//span[@itemprop="text"]/text()').extract()[0]
			author = single_quote.xpath('.//small[@itemprop="author"]/text()').extract()[0]
			item = QuotesItem(
				quote=quote,
				author=author
				)
			yield item
		try:
			next_page= response.xpath('//li[@class="next"]/a/@href').extract()[0]
			yield Request('https://quotes.toscrape.com'+next_page, callback=self.parse)
		except:
			print("No more pages")
			
