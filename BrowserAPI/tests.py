import time
from playwright.sync_api import sync_playwright
import json
import undetected_chromedriver as uc


CHROMIUM_ARGS= [
		'--no-sandbox',
		'--disable-setuid-sandbox',
		'--no-first-run',
		'--disable-blink-features=AutomationControlled'
	  ]
	  
def print_attributes(page):
	#add attributes from https://developer.mozilla.org/en-US/docs/Web/API/Navigator
	cookies=page.evaluate("window.navigator.cookieEnabled")
	print("window.navigator.cookieEnabled: "+ str(cookies))
	memory=page.evaluate("window.navigator.deviceMemory")
	print("window.navigator.deviceMemory: "+str(memory))
	useragent=page.evaluate("window.navigator.userAgent")
	print("window.navigator.userAgent: "+useragent)
	webdriver=page.evaluate("window.navigator.webdriver")
	print("window.navigator.webdriver: "+str(webdriver))
	
	
with sync_playwright() as p:
	#browser = p.chromium.launch_persistent_context(user_data_dir='./userdata/', channel="chrome", headless=False,slow_mo=200, args=CHROMIUM_ARGS,ignore_default_args=["--enable-automation"])
	browser = p.chromium.launch(headless=False,slow_mo=200)
	page = browser.new_page()
	page.on("console", lambda msg: print(msg.text))
	page.goto('https://bot.sannysoft.com/', timeout=0)
	time.sleep(10)
	    # Issue console.log inside the page
	print_attributes(page)
	
driver = uc.Chrome(headless=False,use_subprocess=True)
driver.get("https://bot.sannysoft.com/")
time.sleep(10)