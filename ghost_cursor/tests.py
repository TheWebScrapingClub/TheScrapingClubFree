
import time	
import asyncio
from pyppeteer import launch
from pyppeteer_ghost_cursor import createCursor
import pyppeteer

async def main():
	browser = await pyppeteer.launch(headless=False)
	page = await browser.newPage()
	cursor = createCursor(page)
	await page.goto('https://www.yoox.com/it')
	time.sleep(5)
	
	elements = await page.xpath('//a[@data-tracking-action="kids"]')
	for element in elements:
		cursor.click(element)
	time.sleep(5)
	await browser.close()

asyncio.get_event_loop().run_until_complete(main())