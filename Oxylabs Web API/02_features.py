"""Step 2: test the Web API features one by one. Usage: python 02_features.py <test> [<test> ...]

Each test saves its raw response in artifacts/02_<test>.json and prints the numbers we use in the article.
"""

import json
import sys
import time

from client import ARTIFACTS, WebApiError, describe_scraper, list_scrapers, scrape, scrape_target, search

PRODUCT_URL = "https://www.bestbuy.com/site/sony-wh-1000xm5-wireless-noise-canceling-over-the-ear-headphones-black/6505727.p"
ASIN = "B09XS7JWHH"  # Sony WH-1000XM5 on amazon.com


def save(name, data):
    (ARTIFACTS / f"02_{name}.json").write_text(json.dumps(data, indent=2, ensure_ascii=False))


def timed(fn, *a, **kw):
    t0 = time.time()
    try:
        out = fn(*a, **kw)
    except WebApiError as exc:
        return {"error": str(exc)}, round(time.time() - t0, 1)
    return out, round(time.time() - t0, 1)


def t_discovery():
    data = list_scrapers()
    scrapers = data.get("scrapers", data)
    print("scrapers listed:", len(scrapers))
    sync = [s for s in scrapers if s.startswith("/v1/scrape")]
    print("sync endpoints:", len(sync))
    print("\n".join(sync))
    opts = describe_scraper("scrape/amazon/product")
    print("\nOPTIONS /v1/scrape/amazon/product:\n", json.dumps(opts, indent=1)[:2500])
    save("discovery", {"scrapers": data, "amazon_product_options": opts})


def t_formats():
    out, secs = timed(scrape, PRODUCT_URL, output=["markdown", "html"])
    save("formats", out)
    if "error" in out:
        print("error", out, secs)
        return
    r = out["results"][0]
    print(f"{secs}s  status={r['metadata'].get('statuses')}")
    for fmt in ("html", "markdown"):
        print(f"{fmt}: {len(r.get(fmt) or '')} chars")
    print((r.get("markdown") or "")[:1500])


def t_runjs():
    for run_js in (False, True):
        out, secs = timed(scrape, PRODUCT_URL, output=["markdown"], run_js=run_js)
        save(f"runjs_{run_js}", out)
        if "error" in out:
            print(run_js, out, secs)
            continue
        md = out["results"][0].get("markdown") or ""
        print(f"run_js={run_js}: {secs}s, {len(md)} chars, has '$': {'$' in md}")


def t_location():
    q = "sony wh-1000xm5 price"
    for loc in (None, "US", "DE", "IT"):
        out, secs = timed(search, q, max_results=5, location=loc)
        save(f"location_{loc}", out)
        if "error" in out:
            print(loc, out)
            continue
        print(f"\nlocation={loc} ({secs}s)")
        for r in out["results"]:
            print("  ", r["url"])


SCHEMA = {
    "type": "object",
    "properties": {
        "product_name": {"type": "string"},
        "price": {"type": "number", "description": "Current price the buyer pays, as a number"},
        "currency": {"type": "string", "description": "ISO 4217 code"},
        "availability": {"type": "string", "enum": ["in_stock", "out_of_stock", "preorder", "unknown"]},
        "seller": {"type": "string", "nullable": True},
    },
    "required": ["product_name", "price", "currency", "availability"],
}


def t_aiparse():
    out, secs = timed(scrape, PRODUCT_URL, output=["json"],
                      json={"prompt": "Extract product name, current price as a number, currency and availability"})
    save("aiparse_prompt", out)
    print(f"prompt ({secs}s):", json.dumps(out.get("results", [{}])[0].get("json", out), indent=1)[:1200])
    out, secs = timed(scrape, PRODUCT_URL, output=["json"], json={"schema": SCHEMA})
    save("aiparse_schema", out)
    print(f"schema ({secs}s):", json.dumps(out.get("results", [{}])[0].get("json", out), indent=1)[:1200])


def t_amazon():
    out, secs = timed(scrape_target, "amazon/product", {"query": ASIN, "output": ["json"]})
    save("amazon_product", out)
    if "error" in out:
        print(out, secs)
        return
    j = out["results"][0].get("json") or {}
    print(f"{secs}s, top-level keys ({len(j)}):", sorted(j)[:60])
    for k in ("title", "price", "currency", "stock", "price_buybox", "rating", "reviews_count", "seller_name"):
        print(f"  {k}: {j.get(k)}")


TESTS = {k[2:]: v for k, v in globals().items() if k.startswith("t_")}

if __name__ == "__main__":
    for name in sys.argv[1:] or TESTS:
        print(f"\n===== {name} =====")
        TESTS[name]()
