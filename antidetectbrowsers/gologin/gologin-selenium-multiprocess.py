import time
import os
from multiprocessing import Pool
from sys import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from gologin import GoLogin

def scrap(profile):
	gl = GoLogin({
	        'token': 'yU0token',
	        'profile_id': profile['profile_id'],
	        'port': profile['port'],
		})

	if platform == "linux" or platform == "linux2":
		chrome_driver_path = './chromedriver'
	elif platform == "darwin":
		chrome_driver_path = './mac/chromedriver'
	elif platform == "win32":
		chrome_driver_path = 'chromedriver.exe'

	debugger_address = gl.start()
	chrome_options = Options()
	chrome_options.add_experimental_option("debuggerAddress", debugger_address)
	driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
	driver.get("http://www.python.org")
	print('ready', profile['profile_id'], driver.title)
	time.sleep(10)
	print('closing', profile['profile_id'])
	driver.close()
	gl.stop()

profiles = [
	{'profile_id': 'profile_id_1', 'port': 3500}, 
	{'profile_id': 'profile_id_2', 'port': 3501},
	{'profile_id': 'profile_id_3', 'port': 3502},
	]


with Pool(3) as p:
	p.map(scrap, profiles)


if platform == "win32":
	os.system('taskkill /im chrome.exe /f')
	os.system('taskkill /im chromedriver.exe /f')
else:
	os.system('killall -9 chrome')
	os.system('killall -9 chromedriver')
