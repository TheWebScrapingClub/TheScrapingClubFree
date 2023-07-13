import undetected_chromedriver as uc
import time
from playwright.sync_api import sync_playwright
from gologin import GoLogin
import asyncio
from pyppeteer import launch
from pyppeteer_stealth import stealth



CHROMIUM_ARGS= [
		'--no-sandbox',
		'--disable-setuid-sandbox',
		'--no-first-run',
		'--disable-blink-features=AutomationControlled'
	  ]
with sync_playwright() as p:
	browser = p.chromium.launch_persistent_context(user_data_dir='./userdata/', channel="chrome", headless=False,slow_mo=200, args=CHROMIUM_ARGS,ignore_default_args=["--enable-automation"])
	page = browser.new_page()
	page.goto('https://www.deviceinfo.me/', timeout=0)
	time.sleep(10)
	i=0
	
	while i < 60:
		page.screenshot(path="pl_deviceinfo_"+str(i)+".png")
		page.mouse.wheel(0,500)
		time.sleep(2)
		print(i)
		i=i+1
	

