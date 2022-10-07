import scrapy
from scrapy.http import Request
from bookstoscrape.items import *


class BooksscraperSpider(scrapy.Spider):
	name = 'booksscraper'
	allowed_domains = ['toscrape.com']
	
	
	def start_requests(self):
		start_urls = ['http://books.toscrape.com/']
		for url in start_urls:
			yield Request(url, callback=self.parse)
			
	def parse(self, response):
		BASE_URL='http://books.toscrape.com/'
		book_urls=response.xpath('//article[@class="product_pod"]/h3/a/@href').extract()
		for book_url in book_urls:
			print(BASE_URL+book_url)
			yield Request(BASE_URL+book_url, callback=self.parse_book)
		try:
			next_page=response.xpath('//li[@class="next"]/a/@href').extract()[0]
			yield Request(BASE_URL+next_page, callback=self.parse)
		except:
			pass
	
	def parse_book(self, response):
		
		imageurl=response.xpath('//div[@class="item active"]/img/@src').extract()[0]
		upc=response.xpath('//th[contains(text(), "UPC")]/following-sibling::td[1]/text()').extract()[0]
		producttype=response.xpath('//th[contains(text(), "Product Type")]/following-sibling::td[1]/text()').extract()[0]
		pricenotax=response.xpath('//th[contains(text(), "Price (excl. tax)")]/following-sibling::td[1]/text()').extract()[0]
		pricewithtax=response.xpath('//th[contains(text(), "Price (incl. tax)")]/following-sibling::td[1]/text()').extract()[0]
		availability=response.xpath('//th[contains(text(), "Availability")]/following-sibling::td[1]/text()').extract()[0]
		reviewsnum=response.xpath('//th[contains(text(), "Number of reviews")]/following-sibling::td[1]/text()').extract()[0]
		description=response.xpath('//div[@class="sub-header"]/preceding-sibling::p[1]/text()').extract()[0]
		
		item = BookstoscrapeItem(
			imageurl=imageurl,
			upc=upc,
			producttype=producttype,
			pricenotax=pricenotax,
			pricewithtax=pricewithtax,
			availability=availability,
			reviewsnum=reviewsnum,
			description=description
		)
		yield item
