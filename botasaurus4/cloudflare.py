from botasaurus.browser import browser, Driver
from botasaurus.soupify import soupify
import time

@browser(
	reuse_driver= True,
	#proxy="http://YOURPROXY"
)
def scrape_heading_task(driver: Driver, data):
    # Cloudflare Protected Website
	driver.get("https://www.harrods.com/")
	
	driver.get("https://www.harrods.com/en-it/shopping/women")
	time.sleep(10)
	driver.scroll_to_bottom()

	page_soup = soupify(driver)
	products = page_soup.select('div[data-test="productCard-lazy-load-wrapper"]')
	for product in products:
		try:
			product_name = product.select_one('a > article > h3[data-test="productCard-productName"]').text
			print(f"Product: {product_name}")
		except:
			pass


# Initiate the web scraping task
scrape_heading_task()

#productGrid > div:nth-child(6) > a > article > div.e7gi9o115.css-2pl963.e1wftzrz0 > span

