"""Step 3: ten calls to the Shopee plugin, one attempt each.

Six searches in six markets (one with sort + price filter), then four product calls on items
taken from those searches: two in markets the docs list as "full" (sg, br) and two in markets
listed as "meta" (id, th). Search price vs product price for the same item is a consistency check.
"""

import json
import statistics

from client import ARTIFACTS, shopee_product, shopee_search

SEARCHES = [
    {"q": "iphone case", "country": "sg"},
    {"q": "air fryer", "country": "my", "sort": "sales", "min_price": 100, "max_price": 300},
    {"q": "airpods", "country": "tw"},
    {"q": "fone bluetooth", "country": "br"},
    {"q": "sepatu sneakers", "country": "id"},
    {"q": "power bank", "country": "th"},
]
PRODUCT_MARKETS = ["sg", "br", "id", "th"]

rows, dump, first_items = [], [], {}
for p in SEARCHES:
    r = shopee_search(tag="shopee_search", **p)
    b = r["body"] if isinstance(r["body"], dict) else {}
    prods = b.get("products") or []
    prices = [x["price"] for x in prods if x.get("price") is not None]
    row = {
        "call": "search", **p, "status": r["status"], "elapsed_s": r["elapsed_s"],
        "results": len(prods), "currency": b.get("currency"),
        "price_range": [min(prices), max(prices)] if prices else None,
        "with_discount": sum(1 for x in prods if x.get("discountPercent")),
        "with_labels": sum(1 for x in prods if x.get("labels")),
        "null_rating": sum(1 for x in prods if x.get("rating") is None),
        "error": None if b else str(r["body"] or r.get("error"))[:200],
    }
    if prods:
        first_items[p["country"]] = prods[0]
    rows.append(row)
    dump.append({"params": p, "status": r["status"], "body": r["body"]})
    print(json.dumps(row, ensure_ascii=False))

for country in PRODUCT_MARKETS:
    item = first_items.get(country)
    if not item:
        print(json.dumps({"call": "product", "country": country, "skipped": "no search result"}))
        continue
    p = {"shop_id": item["shopId"], "item_id": item["itemId"], "country": country}
    r = shopee_product(tag="shopee_product", **p)
    b = r["body"] if isinstance(r["body"], dict) else {}
    prod = b.get("product") or {}
    shop = prod.get("shop") or {}
    row = {
        "call": "product", **p, "status": r["status"], "elapsed_s": r["elapsed_s"],
        "data_level": b.get("dataLevel"), "title": (prod.get("title") or "")[:60],
        "search_price": item.get("price"), "product_price": prod.get("price"),
        "images": len(prod.get("images") or []), "has_description": bool(prod.get("description")),
        "variations": len(prod.get("variations") or []), "models": len(prod.get("models") or []),
        "shop_name": shop.get("name"), "shop_rating_count": shop.get("ratingCount"),
        "shop_followers": shop.get("followers"),
        "error": None if b else str(r["body"] or r.get("error"))[:200],
    }
    rows.append(row)
    dump.append({"params": p, "status": r["status"], "body": r["body"]})
    print(json.dumps(row, ensure_ascii=False))

(ARTIFACTS / "03_shopee_results.json").write_text(json.dumps(dump, indent=2, ensure_ascii=False))
(ARTIFACTS / "03_shopee_summary.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False))

ok = [x for x in rows if x.get("status") == 200]
times = [x["elapsed_s"] for x in ok]
print(f"\nsuccess {len(ok)}/{len(rows)}")
if times:
    print(f"latency s: min {min(times)} median {statistics.median(times)} max {max(times)}")
