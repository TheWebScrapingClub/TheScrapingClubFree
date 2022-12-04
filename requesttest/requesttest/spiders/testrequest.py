import scrapy
from scrapy.http import Request
from requesttest.items import *
import json
import requests
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import time

class TestSpider(scrapy.Spider):
	name = 'test'
	
	CUSTOM_REQUEST_HEADERS = {
	   'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	   'accept-language': 'en-US,en;q=0.9',
	   'cache-control': 'max-age=0',
	   'dnt': '1',
	   'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
	   'sec-ch-ua-mobile': '?0',
	   'sec-ch-ua-platform': '"macOS"',
	   'sec-fetch-dest': 'document',
	   'sec-fetch-mode': 'navigate',
	   'sec-fetch-site': 'none',
	   'sec-fetch-user': '?1',
	   'upgrade-insecure-requests': '1',
	   'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
	}
	
	def start_requests(self):
		yield Request('https://www.google.it',callback=self.parse)
			
	def parse(self, response):
		#TEST 1: simple python request with custom headers
		url = "https://webhook.site/3d106682-3d28-4716-b108-f3404c46d3c7"
		response = requests.request("GET", url)
		
		#TEST 2: PLAYWRIGHT FIREFOX NO STEALTH
		with sync_playwright() as p:
			browser = p.firefox.launch(headless=False, slow_mo=300)
			page = browser.new_page()
			page.goto('https://webhook.site/3d106682-3d28-4716-b108-f3404c46d3c7', timeout=0)
			time.sleep(2)
			browser.close()
		
		#TEST 3: PLAYWRIGHT CHROMIUM NO STEALTH
		with sync_playwright() as p:
			browser = p.chromium.launch(headless=False, slow_mo=300)
			page = browser.new_page()
			page.goto('https://webhook.site/3d106682-3d28-4716-b108-f3404c46d3c7', timeout=0)
			time.sleep(2)
			browser.close()
			
		#TEST 4: PLAYWRIGHT CHROMIUM WITH STEALTH
		with sync_playwright() as p:
			browser = p.chromium.launch(headless=False, slow_mo=300)
			page = browser.new_page()
			stealth_sync(page)
			page.goto('https://webhook.site/3d106682-3d28-4716-b108-f3404c46d3c7', timeout=0)
			time.sleep(2)
			browser.close()
		
		#TEST 5: PLAYWRIGHT CHROME NO STEALTH
		with sync_playwright() as p:
			browser = p.chromium.launch_persistent_context(user_data_dir='./userdata/', channel="chrome", headless=False,slow_mo=200)
			page = browser.new_page()
			stealth_sync(page)
			page.goto('https://webhook.site/3d106682-3d28-4716-b108-f3404c46d3c7', timeout=0)
			time.sleep(2)
			browser.close()
		
		#TEST 6: scrapy request with no header set
		yield Request(url,  callback=self.end, dont_filter=True)
		time.sleep(5)
		
		#TEST 7: scrapy request with custom header set
		yield Request(url,  callback=self.end, dont_filter=True, headers=self.CUSTOM_REQUEST_HEADERS)
		time.sleep(5)
		

	
	def end(self, response):
		print("end of tests")