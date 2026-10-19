"""Step 5: find shop pages (no dedicated scraper) whose static Markdown has no price, then confirm with run_js."""

import json
import re
import sys
from urllib.parse import urlparse

from client import ARTIFACTS, WebApiError, list_scrapers, scrape, search

PRODUCT = "Sony WH-1000XM5"
COUNTRIES = sys.argv[1:] or ["US", "GB", "DE", "FR", "IT", "ES", "NL"]
SKIP = ("amazon.", "ebay.", "reddit.", "youtube.", "idealo.", "camelcamelcamel", "rtings", "wikipedia",
        "trovaprezzi", "geizhals", "billiger", "pricespy", "pricerunner", "kelkoo", "google.", "sony.",
        "gizmodo", "techradar", "whathifi", "cnet", "theverge", "tomsguide", "soundguys", "facebook")
PRICE_RE = re.compile(r"(?:[$£€]\s?\d{2,4}(?:[.,]\d{2})?|\d{2,4}(?:[.,]\d{2})?\s?(?:€|EUR))")

dedicated = {s.split("/")[3] for s in list_scrapers()["scrapers"] if s.startswith("/v1/scrape/") and len(s.split("/")) > 3}
rows, seen = [], set()
for cc in COUNTRIES:
    for hit in search(f"{PRODUCT} buy", max_results=20, location=cc)["results"]:
        host = urlparse(hit["url"]).netloc.lower()
        name = host.removeprefix("www.").split(".")[0]
        if host in seen or any(s in host for s in SKIP) or name in dedicated:
            continue
        seen.add(host)
        try:
            md = scrape(hit["url"], output=["markdown"])["results"][0].get("markdown") or ""
        except WebApiError as exc:
            md = ""
            print(f"{cc} {host}: scrape error {exc}")
        prices = PRICE_RE.findall(md)
        row = {"country": cc, "url": hit["url"], "chars": len(md), "prices_static": prices[:8]}
        rows.append(row)
        print(f"{cc} {host}: {len(md)} chars, {len(prices)} prices {prices[:5]}")

for row in rows:
    if row["prices_static"]:
        continue
    try:
        md = scrape(row["url"], output=["markdown"], run_js=True)["results"][0].get("markdown") or ""
        row["chars_js"], row["prices_js"] = len(md), PRICE_RE.findall(md)[:8]
    except WebApiError as exc:
        row["js_error"] = str(exc)
    print("JS check", row)

(ARTIFACTS / "05_js_shops.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False))
