from botasaurus.browser import browser, Driver
from botasaurus.soupify import soupify
import time

@browser(
	reuse_driver= True
)
def scrape_heading_task(driver: Driver, data):
    # Datadome Protected Website
	driver.get('https://abrahamjuliot.github.io/creepjs/')
	time.sleep(50)
	driver.get('https://antoinevastel.com/bots/')
	time.sleep(50)

# Initiate the web scraping task
scrape_heading_task()

#productGrid > div:nth-child(6) > a > article > div.e7gi9o115.css-2pl963.e1wftzrz0 > span

