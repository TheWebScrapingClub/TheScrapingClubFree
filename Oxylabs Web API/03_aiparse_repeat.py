"""Step 3: AI parsing reliability. Same page, prompt vs schema, with and without run_js, 3 runs each."""

import json
import time

from client import ARTIFACTS, WebApiError, scrape

URL = "https://www.bestbuy.com/site/sony-wh-1000xm5-wireless-noise-canceling-over-the-ear-headphones-black/6505727.p"
PROMPT = "Extract product name, current price as a number, currency and availability"
SCHEMA = json.loads((ARTIFACTS.parent / "price_schema.json").read_text())

rows = []
for mode in ("prompt", "schema"):
    for run_js in (False, True):
        for rep in range(3):
            spec = {"prompt": PROMPT} if mode == "prompt" else {"schema": SCHEMA}
            t0 = time.time()
            try:
                out = scrape(URL, output=["json"], json=spec, run_js=run_js)
                parsed = out["results"][0].get("json")
            except WebApiError as exc:
                parsed = {"error": str(exc)}
            row = {"mode": mode, "run_js": run_js, "rep": rep, "secs": round(time.time() - t0, 1), "json": parsed}
            rows.append(row)
            print(json.dumps(row)[:260])

(ARTIFACTS / "03_aiparse_repeat.json").write_text(json.dumps(rows, indent=2))
