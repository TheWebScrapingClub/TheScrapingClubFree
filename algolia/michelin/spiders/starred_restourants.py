import scrapy
from scrapy.http import Request
import json
import csv
from michelin.items import *

class BooksscraperSpider(scrapy.Spider):
	name = 'michelin'
	
	
	def start_requests(self):
		yield Request('https://guide.michelin.com/en/restaurants/all-starred', callback=self.call_api, meta={'page':0})
			
	def call_api(self, response):
		base_url='https://8nvhrd7onv-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(4.19.1)%3B%20Browser%20(lite)%3B%20instantsearch.js%20(4.56.9)%3B%20JS%20Helper%20(3.14.0)&x-algolia-api-key=3222e669cf890dc73fa5f38241117ba5&x-algolia-application-id=8NVHRD7ONV'
		page=response.meta.get('page')
		payload={
			"requests":
			[
				{
					"indexName":"prod-restaurants-en",
					"params":"aroundLatLngViaIP=true&aroundRadius=all&attributesToRetrieve=%5B%22_geoloc%22%2C%22region%22%2C%22area_name%22%2C%22chef%22%2C%22city%22%2C%22country%22%2C%22cuisines%22%2C%22currency%22%2C%22good_menu%22%2C%22identifier%22%2C%22image%22%2C%22main_image%22%2C%22michelin_award%22%2C%22name%22%2C%22slug%22%2C%22new_table%22%2C%22offers%22%2C%22offers_size%22%2C%22online_booking%22%2C%22other_urls%22%2C%22site_slug%22%2C%22site_name%22%2C%22take_away%22%2C%22price_category%22%2C%22currency_symbol%22%2C%22url%22%2C%22green_star%22%5D&facetFilters=%5B%5B%22distinction.slug%3A1-star-michelin%22%2C%22distinction.slug%3A2-stars-michelin%22%2C%22distinction.slug%3A3-stars-michelin%22%5D%5D&facets=%5B%22area_slug%22%2C%22booking_provider%22%2C%22categories.lvl0%22%2C%22city.slug%22%2C%22country.cname%22%2C%22country.slug%22%2C%22cuisines.slug%22%2C%22days_open%22%2C%22delivery%22%2C%22delivery_provider%22%2C%22distinction.slug%22%2C%22facilities.slug%22%2C%22good_menu%22%2C%22green_star.slug%22%2C%22new_table%22%2C%22offers%22%2C%22online_booking%22%2C%22price_category.slug%22%2C%22region.slug%22%2C%22selected_restaurant%22%2C%22take_away%22%5D&filters=status%3APublished&hitsPerPage=20&maxValuesPerFacet=200&page="+str(page)+"&query=&tagFilters="
				},
				{
					"indexName":"prod-restaurants-en",
					"params":"analytics=false&aroundLatLngViaIP=true&aroundRadius=all&attributesToRetrieve=%5B%22_geoloc%22%2C%22region%22%2C%22area_name%22%2C%22chef%22%2C%22city%22%2C%22country%22%2C%22cuisines%22%2C%22currency%22%2C%22good_menu%22%2C%22identifier%22%2C%22image%22%2C%22main_image%22%2C%22michelin_award%22%2C%22name%22%2C%22slug%22%2C%22new_table%22%2C%22offers%22%2C%22offers_size%22%2C%22online_booking%22%2C%22other_urls%22%2C%22site_slug%22%2C%22site_name%22%2C%22take_away%22%2C%22price_category%22%2C%22currency_symbol%22%2C%22url%22%2C%22green_star%22%5D&clickAnalytics=false&facets=distinction.slug&filters=status%3APublished&hitsPerPage=0&maxValuesPerFacet=200&page=0&query="
				}
			]
		}
		#print(json.dumps(payload))
		yield Request(base_url,  callback=self.get_data,method="POST", body=json.dumps(payload), dont_filter=True, meta={'page':response.meta.get('page')})
		
	def get_data(self, response):
		page=response.meta.get('page')
		
		data=json.loads(response.text)
		for restaurant in data['results'][0]['hits']:
			res_id=restaurant['objectID']
			name = restaurant['name']
			chef = restaurant['chef']
			stars = restaurant['michelin_award']
			cuisine_code =restaurant['cuisines']
			try:
				price_category = restaurant['price_category']['slug']
			except:
				price_category = 'n.a.'
			country = restaurant['country']['code']
			region = restaurant['region']['name']
			city = restaurant['city']['name']
			lat  = restaurant['_highlightResult']['_geoloc']['lat']['value']
			lon  = restaurant['_highlightResult']['_geoloc']['lng']['value']
			#print(data)
			item = restaurantItem(
				res_id=res_id,
				name=name,
				chef=chef,
				stars=stars,
				cuisine_code=cuisine_code,
				price_category=price_category,
				country=country,
				region=region,
				city=city,
				lat=lat,
				lon=lon,
				json_data=restaurant
				)
			yield item

		if len(data['results'][0]['hits']) >1:
			page=int(page)+1
			yield Request('https://guide.michelin.com/en/restaurants/all-starred',  callback=self.call_api,  dont_filter=True, meta={'page':page})
			