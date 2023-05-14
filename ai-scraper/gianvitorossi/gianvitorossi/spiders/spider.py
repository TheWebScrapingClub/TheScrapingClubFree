import scrapy
import json

class GianvitoRossiSpider(scrapy.Spider):
    name = 'gianvitorossi'
    start_urls = ['https://www.gianvitorossi.com/it_it']

    def parse(self, response):
        # Extract product categories
        product_pages = response.xpath('//a[@role="menuitem"]/@href').extract()
        for product_page in product_pages:
            yield scrapy.Request(response.urljoin(product_page), callback=self.get_product_list)

    def get_product_list(self, response):
        # Extract product links
        product_links = response.xpath('//a[contains(@class, "b-product_tile-image_link")]/@href')
        for link in product_links:
            yield scrapy.Request(response.urljoin(link.extract()), callback=self.get_product_details)

        # Check for more product pages
        try:
            next_page = response.xpath('//a[data-event-click.prevent="loadMore"]/@href').extract()[0]
            yield scrapy.Request(response.urljoin(next_page), callback=self.get_product_list)
        except:
            pass

    def get_product_details(self, response):
        # Extract JSON data
        json_data = response.xpath('//script[@type="application/ld+json"]/text()').extract_first()
        data = json.loads(json_data)

        # Extract product details
        product_code = data['mpn']
        full_price = data['offers']['price']
        price = full_price
        product_url = response.url

        # Return item
        yield {
            'product_code': product_code,
            'full_price': full_price,
            'price': price,
            'product_url': product_url
        }