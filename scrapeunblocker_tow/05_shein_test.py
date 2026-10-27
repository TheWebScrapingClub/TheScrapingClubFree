"""Step 5: SHEIN, ten calls, one attempt each, a few seconds apart (the docs say SHEIN limits bursts).

The SHEIN plugin has only a search endpoint (US store, first results page, up to 20 products).
So: six searches, one with a price filter and one with sort=price_low, then four product pages
from those searches through /getPageSource with parsed_data=true, to compare the product page
price with the search price.
"""

import json
import statistics
import time

from client import ARTIFACTS, call, page_source

SEARCHES = [
    {"query": "summer dress"},
    {"query": "summer dress", "sort": "price_low", "max_price": 30},
    {"query": "phone case"},
    {"query": "men hoodie", "min_price": 10, "max_price": 30},
    {"query": "kids sneakers"},
    {"query": "wireless earbuds"},
]
PRODUCT_FROM = [0, 2, 3, 4]  # first product of these searches

rows, dump, picks = [], [], []
for i, p in enumerate(SEARCHES):
    r = call("/marketplace/shein-search", p, tag="shein_search")
    b = r["body"] if isinstance(r["body"], dict) else {}
    prods = b.get("products") or []
    prices = [x["price"] for x in prods if x.get("price") is not None]
    lo, hi = p.get("min_price"), p.get("max_price")
    row = {
        "call": "search", **p, "status": r["status"], "elapsed_s": r["elapsed_s"],
        "results": len(prods), "total": b.get("totalResults"),
        "price_range": [min(prices), max(prices)] if prices else None,
        "out_of_filter": sum(1 for x in prices if (lo is not None and x < lo) or (hi is not None and x > hi)),
        "sorted_asc": prices == sorted(prices) if p.get("sort") == "price_low" else None,
        "null_rating": sum(1 for x in prods if x.get("rating") is None),
        "sold_out": sum(1 for x in prods if x.get("soldOut")),
        "error": None if b else str(r["body"] or r.get("error"))[:200],
    }
    if i in PRODUCT_FROM and prods:
        picks.append(prods[0])
    rows.append(row)
    dump.append({"params": p, "status": r["status"], "headers": r.get("headers"), "body": r["body"]})
    print(json.dumps(row, ensure_ascii=False))
    time.sleep(3)

for item in picks:
    r = page_source(item["url"], tag="shein_product", parsed_data="true", proxy_country="us")
    b = r["body"] if isinstance(r["body"], dict) else {}
    d = (b.get("data") or {})
    data = d.get("data") or {}
    price = data.get("price")
    row = {
        "call": "product_page", "id": item["id"], "status": r["status"], "elapsed_s": r["elapsed_s"],
        "headers": r.get("headers"), "page_type": d.get("page_type"), "source": d.get("source"),
        "data_extracted": b.get("data_extracted", True if data else None),
        "search_price": item["price"], "page_price": price,
        "title_match": (data.get("title") or data.get("name") or "")[:40] == item["title"][:40],
        "keys": sorted(data.keys())[:25],
        "error": None if b else str(r["body"] or r.get("error"))[:200],
    }
    rows.append(row)
    dump.append({"params": {"url": item["url"]}, "status": r["status"], "headers": r.get("headers"), "body": r["body"]})
    print(json.dumps(row, ensure_ascii=False))
    time.sleep(3)

(ARTIFACTS / "05_shein_results.json").write_text(json.dumps(dump, indent=2, ensure_ascii=False))
(ARTIFACTS / "05_shein_summary.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False))

ok = [x for x in rows if x.get("status") == 200]
times = [x["elapsed_s"] for x in ok]
print(f"\nsuccess {len(ok)}/{len(rows)}")
if times:
    print(f"latency s: min {min(times)} median {statistics.median(times)} max {max(times)}")
