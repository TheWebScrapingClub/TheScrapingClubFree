from botasaurus.browser import browser, Driver
from botasaurus.soupify import soupify
import time

@browser(
	reuse_driver= True,
	#proxy="http://YOURPROXY"
)
def scrape_heading_task(driver: Driver, data):
    # Datadome Protected Website
	driver.get("https://www.canadagoose.com/")
	time.sleep(5)
	driver.get("https://www.canadagoose.com/us/en/shop/women/outerwear/parkas/")
	time.sleep(10)
	driver.scroll_to_bottom()

	page_soup = soupify(driver)
	products = page_soup.select('div[class="product h-100 bg-white"]')
	for product in products:
		try:
			product_name = product.select_one('div > a[itemprop="url"] > div[itemprop="name"]').text
			print(f"Product: {product_name}")
		except:
			pass


# Initiate the web scraping task
scrape_heading_task()

#productGrid > div:nth-child(6) > a > article > div.e7gi9o115.css-2pl963.e1wftzrz0 > span

