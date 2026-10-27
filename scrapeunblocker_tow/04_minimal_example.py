"""Step 4: the smallest working example for the article, plain requests and nothing else.

One Google SERP and one Shopee search. Every ScrapeUnblocker endpoint is a POST
with the parameters in the query string and the key in the x-scrapeunblocker-key header.
"""

import os

import requests
from dotenv import load_dotenv

load_dotenv()
API = "https://api.scrapeunblocker.com"
HEADERS = {"x-scrapeunblocker-key": os.environ["SCRAPEUNBLOCKER_KEY"]}

serp = requests.post(f"{API}/serpApi", params={"keyword": "assicurazione auto", "proxy_country": "it"},
                     headers=HEADERS, timeout=(10, 125))
serp.raise_for_status()
data = serp.json()
print(data["proxyCountry"], "| organic:", len(data["organic"]), "| ads:", len(data["topAds"]) + len(data["bottomAds"]),
      "| AI Overview:", data["aiOverview"] is not None)
for r in data["organic"][:3]:
    print(r["position"], r["title"][:60], r["url"])

shopee = requests.post(f"{API}/marketplace/shopee-search",
                       params={"q": "iphone case", "country": "sg", "max_results": 3},
                       headers=HEADERS, timeout=(10, 125))
shopee.raise_for_status()
for p in shopee.json()["products"]:
    print(p["position"], p["price"], p["currency"], p["discountPercent"], p["labels"], p["name"][:50])
