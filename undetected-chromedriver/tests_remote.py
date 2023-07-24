import undetected_chromedriver as uc
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#CLOUDFLARE TEST
options = uc.ChromeOptions()
options.binary_location = '/usr/bin/brave-browser'
driver = uc.Chrome(options=options)
driver.get("https://www.harrods.com")
interval = random.randint(5, 15)
time.sleep(interval)
driver.get("https://www.harrods.com/en-it/shopping/women-shoes?icid=megamenu_shop_women_shoes_all-shoes")
test="OK"
interval = random.randint(5, 15)
time.sleep(interval)
while test == "OK":
	try:
		next_page = driver.find_element(By.XPATH, '//a[@title="Next Page"]')
		next_page.click()
		interval = random.randint(5, 15)
		time.sleep(interval)
	except:
		test="FINISH"
		pass

#DATADOME TEST
#options = uc.ChromeOptions()
#options.binary_location = '/usr/bin/brave-browser'
#driver = uc.Chrome(options=options)
#driver.get("https://www.footlocker.it/")
#interval = random.randint(5, 15)
#time.sleep(interval)
#driver.get("https://www.footlocker.it/it/category/bambino/neonati.html")
#test="OK"
#interval = random.randint(5, 15)
#time.sleep(interval)
#while test == "OK":
#	try:
#		next_page = driver.find_element(By.XPATH, '//a[@aria-label="Vai alla pagina successiva"]')
#		next_page.click()
#		interval = random.randint(5, 15)
#		time.sleep(interval)
#	except:
#		test="FINISH"
#		pass

#KASADA TEST
#def scroll_to_end(driver):
     #Scroll down to the end of the page
#    while True:
         #Get current height of the page
#        prev_height = driver.execute_script("return document.body.scrollHeight")

         #Scroll down to the bottom
#        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)

         #Wait for some time for the new content to load
#        time.sleep(2)

         #Get the new height of the page
#        new_height = driver.execute_script("return document.body.scrollHeight")

         #If there is no change in height, it means we have reached the end of the page
#        if new_height == prev_height:
#            break

#options = uc.ChromeOptions()
#options.binary_location = '/usr/bin/brave-browser'
#driver = uc.Chrome(headless=False,use_subprocess=True, options=options)
#driver.get("https://www.canadagoose.com/")
#interval = random.randint(5, 15)
#time.sleep(interval)
#driver.get("https://www.canadagoose.com/it/it/acquista/uomo/capispalla/")
#test="OK"
#interval = random.randint(5, 15)
#time.sleep(interval)
#scroll_to_end(driver)

#PERIMETERX TEST
#options = uc.ChromeOptions()
#options.binary_location = '/usr/bin/brave-browser'
#driver = uc.Chrome(headless=False,use_subprocess=True, options=options)
#driver.get("https://www.neimanmarcus.com/")
#interval = random.randint(5, 15)
#time.sleep(interval)
#try:
#	close_banner=driver.find_element(By.XPATH, '//div[@id="button"]/button')
#	close_banner.click()
#	interval = random.randint(5, 15)
#	time.sleep(interval)
#except:
#	pass
#driver.get("https://www.neimanmarcus.com/c/womens-clothing-clothing-jeans-cat44640769?navpath=cat000000_cat000001_cat58290731_cat44640769")
#test="OK"
#interval = random.randint(5, 15)
#time.sleep(interval)
#while test == "OK":
#	try:
#		next_page = driver.find_element(By.XPATH, '//a[@aria-label="Next"]')
#		next_page.click()
#		interval = random.randint(5, 15)
#		time.sleep(interval)
#	except:
#		test="FINISH"
#		pass

#SHAPE TEST
#driver = uc.Chrome(headless=False,use_subprocess=True)
#driver.get("https://www.nordstrom.com")
#interval = random.randint(5, 15)
#time.sleep(interval)
#try:
#	close_banner=driver.find_element(By.XPATH, '//a[@aria-label="click to close modal"]')
#	close_banner.click()
#	interval = random.randint(5, 15)
#	time.sleep(interval)
#except:
#	pass
#driver.get("https://www.nordstrom.com/browse/women/shoes/espadrilles?breadcrumb=Home%2FShoes%2FWomen%27s%2FEspadrilles&origin=topnav")
#test="OK"
#interval = random.randint(5, 15)
#time.sleep(interval)
#while test == "OK":
#	try:
#		next_page = driver.find_element(By.XPATH, '//li[@class="aGcu6 HHqdE"]/a[@class="OeGVt"]')
#		next_page.click()
#		interval = random.randint(5, 15)
#		time.sleep(interval)
#	except:
#		test="FINISH"
#		pass