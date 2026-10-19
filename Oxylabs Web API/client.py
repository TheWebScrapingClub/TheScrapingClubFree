"""Minimal Oxylabs Web API client, based on the reference client in the official for-agents page.

Every call is appended to artifacts/calls.jsonl with status, latency, request id and payload size,
so the article numbers come from logged runs.
"""

import json
import os
import random
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

HERE = Path(__file__).parent
load_dotenv(HERE / ".env")

API = "https://webapi.oxylabs.io"
RETRYABLE = {408, 429, 500, 502, 503, 504}
ARTIFACTS = HERE / "artifacts"
LOG = ARTIFACTS / "calls.jsonl"
LOG.parent.mkdir(exist_ok=True)


class WebApiError(RuntimeError):
    pass


class AuthenticationError(WebApiError):
    pass


def _headers() -> dict:
    key = os.environ.get("OXYLABS_WEB_API_KEY", "").strip()
    if not key:
        raise WebApiError("OXYLABS_WEB_API_KEY is not set")
    return {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}


def _log(entry: dict) -> None:
    with LOG.open("a") as f:
        f.write(json.dumps(entry) + "\n")


def call(method: str, path: str, payload: dict | None = None, attempts: int = 3) -> dict:
    for attempt in range(1, attempts + 1):
        t0 = time.time()
        try:
            resp = requests.request(method, f"{API}{path}", json=payload, headers=_headers(), timeout=180)
        except requests.Timeout as exc:
            _log({"ts": t0, "path": path, "payload": payload, "status": "timeout", "attempt": attempt})
            if attempt == attempts:
                raise WebApiError(f"{path} timed out after {attempts} attempts") from exc
            time.sleep(2**attempt + random.random())
            continue
        elapsed = round(time.time() - t0, 2)
        try:
            body = resp.json()
        except ValueError:
            body = {"raw": resp.text[:500]}
        meta = body.get("metadata", {}) if isinstance(body, dict) else {}
        _log({
            "ts": t0, "path": path, "payload": payload, "status": resp.status_code,
            "attempt": attempt, "elapsed_s": elapsed, "bytes": len(resp.content),
            "request_id": meta.get("request_id"),
            "error_title": body.get("title") if not resp.ok and isinstance(body, dict) else None,
        })
        if resp.ok:
            return body
        if resp.status_code == 401:
            raise AuthenticationError("401: the API key was rejected")
        if resp.status_code not in RETRYABLE or attempt == attempts:
            detail = f"{body.get('title')}: {body.get('detail')} {body.get('errors', '')}" if isinstance(body, dict) else ""
            raise WebApiError(f"{path} -> {resp.status_code}: {detail}")
        time.sleep(2**attempt + random.random())
    raise WebApiError("unreachable")


def search(query: str, max_results: int = 10, location: str | None = None) -> dict:
    payload = {"query": query, "max_results": max_results}
    if location:
        payload["location"] = location
    return call("POST", "/v1/search", payload)


def scrape(url: str, output: list[str] | None = None, attempts: int = 3, **extra) -> dict:
    payload = {"url": url, "output": output or ["markdown"], **extra}
    return call("POST", "/v1/scrape", payload, attempts=attempts)


def scrape_target(endpoint: str, params: dict) -> dict:
    return call("POST", f"/v1/scrape/{endpoint.strip('/')}", params)


def list_scrapers() -> dict:
    return call("GET", "/v1/scrapers")


def describe_scraper(endpoint: str) -> dict:
    return call("OPTIONS", f"/v1/{endpoint.strip('/')}")
