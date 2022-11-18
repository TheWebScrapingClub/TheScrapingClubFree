import time
import asyncio
import pyppeteer
from sys import platform
from gologin import GoLogin

async def main():
	gl = GoLogin({
		"token": "yU0token",
		"profile_id": "yU0Pr0f1leiD",
		})

	debugger_address = gl.start()
	browser = await pyppeteer.connect(browserURL="http://"+debugger_address)
	page = await browser.newPage()
	await gl.normalizePageView(page)
	await page.goto('https://gologin.com')
	await page.screenshot({'path': 'gologin.png'})
	await browser.close()
	gl.stop()

asyncio.get_event_loop().run_until_complete(main())
