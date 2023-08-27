
from playwright.sync_api import sync_playwright
from scrapy.http import HtmlResponse
import time
import csv
from random import randrange
import random
import json
from datetime import datetime
import sys


CHROMIUM_ARGS= [
		'--no-first-run',
		'--disable-blink-features=AutomationControlled'
		#'--profile-directory='+path_to_profile
	  ]
	

with sync_playwright() as p:
	browser = p.firefox.launch_persistent_context(user_data_dir='./userdata/',
		headless=False,slow_mo=200, args=CHROMIUM_ARGS,
		ignore_default_args=["--enable-automation"],
		
		
	)
	page = browser.new_page()
	page.goto('https://www.google.com/recaptcha/api2/demo', timeout=0)
	time.sleep(60)

	try:
		page.locator("xpath=//input[@id='recaptcha-demo-submit']").click()
		interval=randrange(10)
		time.sleep(interval)
	except:
		pass
			
	browser.close()
			