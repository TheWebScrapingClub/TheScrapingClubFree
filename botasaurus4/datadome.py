from botasaurus.browser import browser, Driver
from botasaurus.soupify import soupify
import time

@browser(
	reuse_driver= True,
	#proxy="http://YOURPROXY"
)
def scrape_heading_task(driver: Driver, data):
    # Datadome Protected Website
	driver.get("https://www.footlocker.it/")
	
	driver.get("https://www.footlocker.it/it/category/uomo/scarpe.html")
	time.sleep(10)
	driver.scroll_to_bottom()

	page_soup = soupify(driver)
	products = page_soup.select('div[class="ProductCard ProductCard--flexDirection"]')
	for product in products:
		try:
			product_name = product.select_one('a > span[class="ProductName"] > span').text
			print(f"Product: {product_name}")
		except:
			pass


# Initiate the web scraping task
scrape_heading_task()

#productGrid > div:nth-child(6) > a > article > div.e7gi9o115.css-2pl963.e1wftzrz0 > span

