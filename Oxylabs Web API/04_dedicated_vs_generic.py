"""Step 4: Best Buy and Walmart dedicated scrapers vs the generic /v1/scrape on the same product."""

import json
import time

from client import ARTIFACTS, WebApiError, scrape_target

CASES = [
    ("bestbuy/product", {"query": "6505727"}),
    ("bestbuy", {"url": "https://www.bestbuy.com/site/sony-wh-1000xm5-wireless-noise-canceling-over-the-ear-headphones-black/6505727.p"}),
    ("walmart/product", {"query": "386006068"}),
    ("walmart", {"url": "https://www.walmart.com/ip/Sony-WH-1000XM5-The-Best-Wireless-Noise-Canceling-Headphones-Black/386006068"}),
]
PRICE_KEYS = ("title", "price", "price_strikethrough", "currency", "availability", "stock", "seller", "rating")

results = {}
for endpoint, params in CASES:
    t0 = time.time()
    try:
        out = scrape_target(endpoint, {**params, "output": ["json"]})
        j = out["results"][0].get("json") or {}
    except WebApiError as exc:
        j = {"error": str(exc)}
    secs = round(time.time() - t0, 1)
    results[endpoint] = {"secs": secs, "json": j}
    print(f"\n== {endpoint} {params} -> {secs}s, {len(j)} top-level keys")
    print("keys:", sorted(j)[:40])
    print({k: j.get(k) for k in PRICE_KEYS if k in j})

(ARTIFACTS / "04_dedicated.json").write_text(json.dumps(results, indent=2, ensure_ascii=False))
