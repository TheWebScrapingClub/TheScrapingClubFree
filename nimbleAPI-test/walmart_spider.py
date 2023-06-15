import requests
import json
import csv

DEFAULT_VALUE='n.a.'
url = 'https://api.webit.live/api/v1/realtime/ecommerce'
headers = {
    'Authorization': 'Basic TOKEN',
    'Content-Type': 'application/json'
}

check = 1
index = 1
while check > 0:
	data = {
		"parse": True, 
		"vendor": "walmart", 
		"url": "https://www.walmart.com/search?q=nike+air+jordan+1+mid&affinityOverride=default&page="+str(index), 
		"format": "json", 
		"render": True, 
		"country": "ALL", 
		"locale": "en"
	}

	response = requests.post(url, headers=headers, json=data)

	print(response.status_code)
	print(response.json())
	response_data=json.loads(response.text)
	print(response_data['parsing'])
	#MULTIPLE OFFERS PAGE
	for product in response_data['parsing']['entities']['SearchResult']:
		try:
			name=product['name']
		except:
			name=DEFAULT_VALUE
		try:
			imageurl=product['image']
		except:
			imageurl=DEFAULT_VALUE
		try:
			offer_id=product['offerId']
		except:
			offer_id=DEFAULT_VALUE
		try:
			merchant_name=product['sellerName']
		except:
			merchant_name=DEFAULT_VALUE
		currency='USD'
		country='USA'
		try:
			price=product['price']
		except:
			price=DEFAULT_VALUE
		try:
			itemurl='https://www.walmart.com'+product['canonicalUrl']
		except:
			itemurl=DEFAULT_VALUE
		try:
			sku=product['id']
		except:
			sku=DEFAULT_VALUE
		
		with open("walmart.txt", "a") as file:
			csv_file = csv.writer(file, delimiter="|")
			csv_file.writerow([name,imageurl,offer_id ,merchant_name,price,currency,country,itemurl,sku])
		file.close()
	if len(response_data['parsing']['entities']['SearchResult']) >= 40 and index < 26:
		index = index+1
	else:
		check = 0
