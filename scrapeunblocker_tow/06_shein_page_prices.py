"""Step 6: raw HTML of two SHEIN product pages whose parsed price differs from the search price.

Looks for both values (search price and parsed page price) in the HTML and prints the context
around each hit, to see where each number comes from on the page.
"""

import json
import re
import sys

from client import ARTIFACTS, page_source

CASES = [
    ("68261159", "https://us.shein.com/Children-s-Sports-Shoes-Casual-Running-Sneakers-Breathable-Mesh-Lightweight-Non-slip-For-Boys-And-Girls-p-68261159.html", "12.40", "17.70"),
    ("559986897", None, "10.08", "13.08"),
]

results = json.load(open(ARTIFACTS / "05_shein_results.json"))
urls = {e["body"]["products"][0]["id"]: e["body"]["products"][0]["url"] for e in results[:6] if isinstance(e["body"], dict)}

for gid, _, search_price, page_price in CASES:
    url = urls[gid]
    r = page_source(url, tag="shein_html", proxy_country="us")
    html = r["body"] if isinstance(r["body"], str) else ""
    (ARTIFACTS / f"06_shein_{gid}.html").write_text(html)
    print(f"== {gid} status {r['status']} {r['elapsed_s']}s {len(html)} chars")
    for label, value in (("search", search_price), ("page", page_price)):
        hits = [m.start() for m in re.finditer(re.escape(value), html)]
        print(f"  {label} price {value}: {len(hits)} hits")
        for h in hits[:4]:
            print("    ...", re.sub(r"\s+", " ", html[max(0, h - 120):h + 40]))
    sys.stdout.flush()
