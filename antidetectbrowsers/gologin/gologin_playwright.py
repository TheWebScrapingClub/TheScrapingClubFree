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
	"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2M2JkOGZlYjQzN2Q1MDFjNjIzNTZiZmUiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2M2JkOTAzYzI2ZDA0MzZhNjM1MTVhZDAifQ.z3fsylpNK1lBBpdfZTakvS6NHFxZkkbaZoM51oXIz5g",
	"profile_id": "63bd8feb437d50a3c0356c3f",
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
