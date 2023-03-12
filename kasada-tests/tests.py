import undetected_chromedriver as uc
import time
from playwright.sync_api import sync_playwright
from gologin import GoLogin
import asyncio
from pyppeteer import launch
from pyppeteer_stealth import stealth



driver = uc.Chrome()
driver.get("https://www.canadagoose.com/us/en/home-page")
driver.set_window_size(1000, 900)
time.sleep(10)
driver.save_screenshot('uc_kasada.png')

CHROMIUM_ARGS= [
		'--no-sandbox',
		'--disable-setuid-sandbox',
		'--no-first-run',
		'--disable-blink-features=AutomationControlled'
	  ]
with sync_playwright() as p:
	browser = p.chromium.launch_persistent_context(user_data_dir='./userdata/', channel="chrome", headless=False,slow_mo=200, args=CHROMIUM_ARGS,ignore_default_args=["--enable-automation"])
	page = browser.new_page()
	page.goto('https://www.canadagoose.com/us/en/home-page', timeout=0)
	time.sleep(10)
	page.screenshot(path="pl_kasada.png")

	
with sync_playwright() as p:
	browser = p.firefox.launch(headless=False, slow_mo=300)
	page = browser.new_page()
	page.goto('https://www.canadagoose.com/us/en/home-page', timeout=0)
	time.sleep(10)
	page.screenshot(path="pl_f_kasada.png")

gl = GoLogin({
	"token": "YOUR TOKEN",
	"profile_id": 'PROFILE ID TO ATTACH',
})
debugger_address = gl.start()
with sync_playwright() as p:
	browser = p.chromium.connect_over_cdp("http://"+debugger_address)
	page = browser.new_page()
	gl.normalizePageView(page)
	page.goto('https://www.canadagoose.com/us/en/home-page', timeout=0)
	time.sleep(10)
	page.screenshot(path="pl_g_kasada.png")
	browser.close()
	
async def main():
	browser = await launch(headless=False)
	page = await browser.newPage()
	await stealth(page)
	await page.goto("https://www.canadagoose.com/us/en/home-page")
	time.sleep(10)
	await page.screenshot({'path': 'py_kasada.png'})
	await browser.close()
asyncio.get_event_loop().run_until_complete(main())