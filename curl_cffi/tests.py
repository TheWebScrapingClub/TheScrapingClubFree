from curl_cffi import requests

# Notice the impersonate parameter
r = requests.get("https://www.harrods.com/en-it/shopping/women-clothing-dresses?icid=megamenu_shop_women_dresses_all-dresses", impersonate="chrome110")
print(r.text)