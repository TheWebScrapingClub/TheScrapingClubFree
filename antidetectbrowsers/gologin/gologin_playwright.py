#THIS IS A TEMPLATE SPIDER FOR WHAT WE CALL PHASE A
#ITEMS, LOGGING SYSTEM AND OUTPUT FILES WILL HAVE ALWAYS THE 
#SAME STRUCTURE AND BEHAVIOUR FOR EVERY SPIDER IN PHASE A


import time
from sys import platform
from gologin import GoLogin
from playwright.sync_api import sync_playwright
from scrapy.http import HtmlResponse
import time
import csv
from random import randrange
import random
from playwright_stealth import stealth_sync
from datetime import datetime



gl = GoLogin({
	"token": "YOURTOKEN",
	"profile_id": "YOURPROFILEID",
	})

debugger_address = gl.start()
with sync_playwright() as p:
	browser = p.chromium.connect_over_cdp("http://"+debugger_address)
	page = browser.new_page()
	gl.normalizePageView(page)
	page.goto('https://www.off---white.com/')
	time.sleep(5)
	page.goto('https://www.off---white.com/it-it/shopping/woman')
	time.sleep(30)
	browser.close()
	gl.stop()
