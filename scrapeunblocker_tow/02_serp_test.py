"""Step 2: ten Google SERPs through /serpApi, one page each, one attempt each.

Mix of commercial (ads expected), informational (AI Overview expected) and local queries,
across nine countries. "br" is not in the documented SERP country list: the docs say the
call falls back to another exit and adds requestedCountry + note instead of failing.
"""

import json
import statistics

from client import ARTIFACTS, serp

QUERIES = [
    ("best running shoes", "us"),
    ("iphone 17 pro price", "us"),
    ("how do solar panels work", "gb"),
    ("assicurazione auto", "it"),
    ("pizza in der nähe", "de"),
    ("web scraping python", None),
    ("hotel tokyo shinjuku", "jp"),
    ("cashback credit card", "ca"),
    ("mejores auriculares inalambricos", "es"),
    ("seguro de carro", "br"),
]
AD_MARKERS = ("googleadservices.com", "/aclk?", "google.com/aclk")

rows, bodies = [], []
for kw, country in QUERIES:
    params = {"proxy_country": country} if country else {}
    r = serp(kw, tag="serp", **params)
    b = r.get("body") if isinstance(r.get("body"), dict) else {}
    organic = b.get("organic") or []
    urls = [o.get("url") or "" for o in organic]
    row = {
        "keyword": kw, "asked": country, "status": r["status"], "elapsed_s": r["elapsed_s"],
        "served": b.get("proxyCountry"), "requested": b.get("requestedCountry"), "note": b.get("note"),
        "organic": len(organic), "top_ads": len(b.get("topAds") or []), "bottom_ads": len(b.get("bottomAds") or []),
        "ai_overview": b.get("aiOverview") is not None, "total_results": b.get("totalResults"),
        "pages": b.get("pagesFetched"), "dup_urls": len(urls) - len(set(urls)),
        "ad_urls_in_organic": sum(any(m in u for m in AD_MARKERS) for u in urls),
        "error": None if b else str(r.get("body") or r.get("error"))[:200],
    }
    rows.append(row)
    bodies.append({"keyword": kw, "asked": country, "status": r["status"], "body": r.get("body")})
    print(json.dumps(row, ensure_ascii=False))

(ARTIFACTS / "02_serp_results.json").write_text(json.dumps(bodies, indent=2, ensure_ascii=False))
(ARTIFACTS / "02_serp_summary.json").write_text(json.dumps(rows, indent=2, ensure_ascii=False))

ok = [x for x in rows if x["status"] == 200]
times = [x["elapsed_s"] for x in ok]
print(f"\nsuccess {len(ok)}/{len(rows)}")
if times:
    print(f"latency s: min {min(times)} median {statistics.median(times)} max {max(times)}")
print("with ads:", sum(1 for x in ok if x["top_ads"] or x["bottom_ads"]),
      "| with AI Overview:", sum(x["ai_overview"] for x in ok),
      "| organic per page:", [x["organic"] for x in ok])
