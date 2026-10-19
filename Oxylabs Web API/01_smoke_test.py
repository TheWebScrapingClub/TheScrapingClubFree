"""Step 1: one real search, then a scrape of the first result as Markdown."""

import json

from client import ARTIFACTS, scrape, search

hits = search("oxylabs web api pricing", max_results=5)
print("search request_id:", hits["metadata"]["request_id"])
for r in hits["results"]:
    print(f"  #{r['metadata']['position']} {r['title'][:70]} | {r['url']}")
print("related_searches:", [s["query"] for s in hits.get("related_searches", [])][:5])

first = hits["results"][0]["url"]
page = scrape(first, output=["markdown"])
res = page["results"][0]
print("\nscrape request_id:", page.get("metadata", {}).get("request_id"))
print("result keys:", sorted(res.keys()))
print("final url:", res.get("url"))
print("markdown chars:", len(res.get("markdown") or ""))
print((res.get("markdown") or "")[:800])

(ARTIFACTS / "01_search.json").write_text(json.dumps(hits, indent=2))
(ARTIFACTS / "01_scrape.json").write_text(json.dumps(page, indent=2))
