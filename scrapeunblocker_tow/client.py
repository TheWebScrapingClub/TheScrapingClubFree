"""Minimal ScrapeUnblocker client on plain requests.

One attempt per call by default, so the success rates in the article are raw, not retried.
Every call is appended to artifacts/calls.jsonl with status, latency, size and the
ScrapeUnblocker headers that explain an answer (X-Origin-Status, X-SU-Error-Code, ...).
"""

import json
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

HERE = Path(__file__).parent
load_dotenv(HERE / ".env")

API = "https://api.scrapeunblocker.com"
ARTIFACTS = HERE / "artifacts"
LOG = ARTIFACTS / "calls.jsonl"
LOG.parent.mkdir(exist_ok=True)
SU_HEADERS = ("X-Origin-Status", "X-SU-Error-Code", "X-SU-Served-Url", "X-SU-Deny-Reason",
              "X-ScrapeUnblocker-Note", "Retry-After", "Content-Type")


def _key() -> str:
    key = os.environ.get("SCRAPEUNBLOCKER_KEY", "").strip()
    if not key:
        raise RuntimeError("SCRAPEUNBLOCKER_KEY is not set")
    return key


def _log(entry: dict) -> None:
    with LOG.open("a") as f:
        f.write(json.dumps(entry) + "\n")


def call(path: str, params: dict, tag: str = "", send_key: bool = True) -> dict:
    """POST to an endpoint with query-string params. Returns status, latency, headers and body."""
    headers = {"x-scrapeunblocker-key": _key()} if send_key else {}
    t0 = time.time()
    try:
        resp = requests.post(f"{API}{path}", params=params, headers=headers, timeout=(10, 180))
    except requests.RequestException as exc:
        out = {"tag": tag, "path": path, "params": params, "status": "error",
               "error": repr(exc), "elapsed_s": round(time.time() - t0, 2)}
        _log({"ts": t0, **out})
        return out
    elapsed = round(time.time() - t0, 2)
    try:
        body = resp.json()
    except ValueError:
        body = resp.text
    su = {h: resp.headers[h] for h in SU_HEADERS if h in resp.headers}
    out = {"tag": tag, "path": path, "params": params, "status": resp.status_code,
           "elapsed_s": elapsed, "bytes": len(resp.content), "headers": su, "body": body}
    _log({"ts": t0, **{k: v for k, v in out.items() if k != "body"},
          "body_head": body[:300] if isinstance(body, str) else None})
    return out


def page_source(url: str, tag: str = "", **params) -> dict:
    return call("/getPageSource", {"url": url, **params}, tag)


def serp(keyword: str, tag: str = "", **params) -> dict:
    return call("/serpApi", {"keyword": keyword, **params}, tag)


def shopee_search(tag: str = "", **params) -> dict:
    return call("/marketplace/shopee-search", params, tag)


def shopee_product(tag: str = "", **params) -> dict:
    return call("/marketplace/shopee-product", params, tag)
