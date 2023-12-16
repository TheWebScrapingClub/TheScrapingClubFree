import scrapy


class EcomscraperSpider(scrapy.Spider):
	name = "ecomscraper"
	allowed_domains = ["valentino.com"]
	start_urls = ["https://www.valentino.com/en-gb"]

	def parse(self, response):
		categories = response.xpath('//a[@class="column-element"]/@href').extract()
		for category in categories:
			print(category)
		pass
