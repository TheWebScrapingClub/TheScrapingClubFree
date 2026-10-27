"""Step 1: auth check (free) and the vendor's own pricing page, which a plain client cannot read.

A direct GET of scrapeunblocker.com/pricing returns a Vercel Security Checkpoint page,
so the pricing page doubles as a first unblocking test.
"""

import requests

from client import ARTIFACTS, call, page_source

direct = requests.get("https://scrapeunblocker.com/pricing",
                      headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}, timeout=30)
print("direct GET:", direct.status_code, "| checkpoint page:", "Vercel Security Checkpoint" in direct.text)

no_key = call("/getPageSource", {"url": "https://example.com"}, tag="no_key", send_key=False)
print("without key:", no_key["status"], repr(no_key["body"])[:60])

r = page_source("https://scrapeunblocker.com/pricing", tag="pricing", markdown="true")
print("via API:", r["status"], f"{r['elapsed_s']}s", r["bytes"], "bytes", r["headers"])
if isinstance(r["body"], str):
    (ARTIFACTS / "01_pricing.md").write_text(r["body"])
    print("checkpoint page:", "Vercel Security Checkpoint" in r["body"])
    print(r["body"][:3000])
