from botasaurus import *
from lxml import etree 
import json
import time
from random import randrange
from botasaurus.create_stealth_driver import create_stealth_driver
from capsolver_extension_python import Capsolver
from selenium.webdriver.common.by import By

@browser(
	user_agent=bt.UserAgent.REAL, 
	window_size=bt.WindowSize.REAL,
	create_driver=create_stealth_driver(
	start_url="https://www.footlocker.it",
	),
	
)

def scrape_heading_task(driver: AntiDetectDriver, data):
	interval=randrange(10)
	time.sleep(interval)
	driver.get("https://www.footlocker.it/it/category/uomo/scarpe/sneakers.html")
	interval=randrange(10)
	time.sleep(interval)
	# Retrieve the heading element's text
	url_list_data=driver.find_elements(By.XPATH,'//a[contains(@class, "ProductCard-link")]')
	url_list_final=[]
	for url_list in url_list_data:
		url=url_list.get_attribute('href')
		print(url)
		url_list_final.append(url)
		
	for url in url_list_final:
		driver.get(url)
		price=driver.find_element(By.XPATH,'//script[@id="productLdJson"]').text
		print(price)
		interval=randrange(10)
		time.sleep(interval)

scrape_heading_task()
