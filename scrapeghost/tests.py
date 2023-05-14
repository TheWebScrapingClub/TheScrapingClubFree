from scrapeghost import SchemaScraper, XPath
import csv



schema_left={
	  "product_name": "text",
	  "price" : "text",
	  "price_without_discounts" : "text",

}

scrape_prod_details_left = SchemaScraper(
  schema_left,
  extra_preprocessors=[XPath('//section[@class="productInfo"]')],
)

schema_desc={
	  "description": "text",
	  "product_code" : "text",
}

scrape_prod_details_desc = SchemaScraper(
  schema_desc,
  extra_preprocessors=[XPath('//section[contains(@class, "productDescription")]')],
)

schema_right={
	  "color_name" : "text"
}

scrape_prod_details_right = SchemaScraper(
  schema_right,
  extra_preprocessors=[XPath('//section[@class="pdpColorSelection"]')],
  extra_instructions=["Put the color name in the color_name field"],
  
)

url_file = open('urls.txt')
LOCATIONS = url_file.readlines()
for url in LOCATIONS:
	try:
		resp = scrape_prod_details_left(url)
		data_left=resp.data
		resp = scrape_prod_details_desc(url)
		data_desc=resp.data
		resp = scrape_prod_details_right(url)
		data_right=resp.data
		
		try:
			product_name= data_left['product_name']
		except:
			product_name= data_left[0]['product_name']
		try:
			description = data_desc['description'].replace('\n', ' ')
		except:
			description = data_desc[0]['description'].replace('\n', ' ')
		try:
			price = data_left['price']
		except:
			price = data_left[0]['price']
		try:
			price_full = data_left['price_without_discounts']
		except:
			price_full = data_left[0]['price_without_discounts']
		try:
			productcode = data_desc['product_code']
		except:
			productcode = data_desc[0]['product_code']
		try:
			color = data_right['color_name']
		except:
			color = data_right[0]['color_name']
		
		with open("products.txt", "a") as file_b:
			csv_file_b = csv.writer(file_b, delimiter="|")
			csv_file_b.writerow([product_name,description,price,price_full,productcode,data_right ])
		file_b.close()
	except:
		pass