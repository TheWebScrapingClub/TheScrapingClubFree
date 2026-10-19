"""Price research agent: Claude + Oxylabs Web API.

Given a product, the agent searches the web, picks 3 shops and reads the current price from each one.
It stops after 3 results. Every tool call is printed and saved in artifacts/agent_run_<ts>.json.

Usage: python agent.py "Sony WH-1000XM5" US [url1 url2 url3]
With URLs the agent skips the search and reads those shop pages.
"""

import json
import sys
import time

import anthropic

from client import ARTIFACTS, WebApiError, scrape, scrape_target, search

MODEL = "claude-opus-5-5"
MAX_PAGE_CHARS = 60_000
PRICE_SCHEMA = json.loads((ARTIFACTS.parent / "price_schema.json").read_text())

TOOLS = [
    {
        "name": "web_search",
        "description": "Search the live web (Oxylabs /v1/search). Returns title, url and short snippets. "
                       "Snippets are truncated: use them only to choose which page to read.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "location": {"type": "string", "description": "ISO 3166-1 alpha-2 country code, e.g. US"},
            },
            "required": ["query"],
        },
    },
    {
        "name": "scrape_page",
        "description": "Read any URL as Markdown (Oxylabs generic /v1/scrape). Fast without JavaScript. "
                       "If the price or the main content is missing, call it again with run_js=true "
                       "(real browser render, 20-40 seconds).",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string"},
                "run_js": {"type": "boolean", "default": False},
            },
            "required": ["url"],
        },
    },
    {
        "name": "extract_product",
        "description": "Extract product_name, price, currency, availability and seller from a product page as JSON, "
                       "using Oxylabs AI parsing with a fixed schema. Costs more than scrape_page. "
                       "A null price means the parser did not find it: try again with run_js=true.",
        "input_schema": {
            "type": "object",
            "properties": {
                "url": {"type": "string"},
                "run_js": {"type": "boolean", "default": False},
            },
            "required": ["url"],
        },
    },
    {
        "name": "amazon_product",
        "description": "Amazon product data from the Oxylabs dedicated scraper, by ASIN. Returns parsed JSON "
                       "(title, price, buybox, stock, rating). Use it instead of scrape_page for Amazon.",
        "input_schema": {
            "type": "object",
            "properties": {
                "asin": {"type": "string"},
                "domain": {"type": "string", "description": "Amazon TLD, e.g. com, de, it", "default": "com"},
            },
            "required": ["asin"],
        },
    },
    {
        "name": "bestbuy_product",
        "description": "Best Buy product data from the Oxylabs dedicated scraper, by SKU (the number in the URL, "
                       "e.g. 6505727). Returns parsed JSON (title, price, is_sold_out, rating). "
                       "Use it instead of scrape_page for Best Buy.",
        "input_schema": {
            "type": "object",
            "properties": {"sku": {"type": "string"}},
            "required": ["sku"],
        },
    },
]

SYSTEM = """You are a price research agent. The user gives you a product and a country.
Find the current price of that exact product in 3 different online shops of that country, then stop.

Rules:
- Start with one web_search. Choose shop product pages, not reviews, forums or price trackers.
- Read prices only from pages you scraped. Never use search snippets or your memory for a price.
- For Amazon use amazon_product, for Best Buy use bestbuy_product. For other shops use scrape_page first.
- If scrape_page fails or returns a page without the product price, call it again with run_js=true.
- Use extract_product only when the Markdown is ambiguous.
- If a page fails twice, report it as failed and pick another shop.
- Stop as soon as you have 3 prices.
- If the user lists shop URLs, skip the search and read exactly those pages.

Final answer: a JSON array with one object per shop:
{"shop", "url", "price", "currency", "availability", "tool_used", "run_js"}
followed by one short line on anything that failed."""


def run_tool(name: str, args: dict) -> dict:
    if name == "web_search":
        out = search(args["query"], max_results=10, location=args.get("location"))
        return {"results": [{"title": r["title"], "url": r["url"], "outline": r.get("outline", [])[:1]}
                            for r in out["results"]]}
    if name == "scrape_page":
        # Oxylabs already retries a failed scrape server-side before answering 500,
        # so the agent gets the error once and decides what to do (usually run_js=true).
        out = scrape(args["url"], output=["markdown"], run_js=bool(args.get("run_js")), attempts=1)
        md = out["results"][0].get("markdown") or ""
        result = {"chars": len(md), "markdown": md[:MAX_PAGE_CHARS]}
        if len(md) > MAX_PAGE_CHARS:
            # Rendered pages can start with 100K+ chars of menus: start from the first H1 (the product title).
            h1 = md.find("\n# ")
            start = h1 if h1 > 0 else 0
            result["markdown"] = md[start:start + MAX_PAGE_CHARS]
            result["note"] = f"{len(md)} chars, showing {start}-{start + MAX_PAGE_CHARS} (from the first H1)"
        return result
    if name == "extract_product":
        out = scrape(args["url"], output=["json"], json={"schema": PRICE_SCHEMA}, run_js=bool(args.get("run_js")))
        return out["results"][0].get("json") or {}
    if name == "amazon_product":
        out = scrape_target("amazon/product", {"query": args["asin"], "domain": args.get("domain", "com"),
                                               "output": ["json"]})
        j = out["results"][0].get("json") or {}
        keep = ("title", "price", "price_buybox", "currency", "stock", "rating", "reviews_count", "url")
        return {k: j.get(k) for k in keep}
    if name == "bestbuy_product":
        out = scrape_target("bestbuy/product", {"query": args["sku"], "output": ["json"]})
        return out["results"][0].get("json") or {}
    raise ValueError(f"unknown tool {name}")


def main(product: str, country: str, urls: list[str]) -> None:
    client = anthropic.Anthropic()
    prompt = f"Product: {product}\nCountry: {country}"
    if urls:
        prompt += "\nShop URLs:\n" + "\n".join(urls)
    messages = [{"role": "user", "content": prompt}]
    trace, t_start = [], time.time()
    usage = {"input_tokens": 0, "output_tokens": 0}

    for turn in range(20):
        response = client.messages.create(
            model=MODEL, max_tokens=16000, system=SYSTEM, tools=TOOLS, messages=messages,
        )
        usage["input_tokens"] += response.usage.input_tokens
        usage["output_tokens"] += response.usage.output_tokens
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            final = "".join(b.text for b in response.content if b.type == "text")
            print("\n=== FINAL ANSWER ===\n" + final)
            break

        results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            t0 = time.time()
            try:
                output, is_error = run_tool(block.name, block.input), False
            except (WebApiError, KeyError, IndexError, ValueError) as exc:
                output, is_error = {"error": str(exc)}, True
            secs = round(time.time() - t0, 1)
            summary = {k: v for k, v in output.items() if k != "markdown"} if isinstance(output, dict) else output
            print(f"[turn {turn}] {block.name}({json.dumps(block.input)}) -> {secs}s "
                  f"{json.dumps(summary, ensure_ascii=False)[:300]}")
            trace.append({"turn": turn, "tool": block.name, "input": block.input, "secs": secs,
                          "is_error": is_error, "output_summary": summary})
            results.append({"type": "tool_result", "tool_use_id": block.id,
                            "content": json.dumps(output, ensure_ascii=False), "is_error": is_error})
        messages.append({"role": "user", "content": results})
    else:
        final = "stopped: turn limit reached"

    total = round(time.time() - t_start, 1)
    print(f"\ntotal {total}s, tool calls {len(trace)}, tokens {usage}")
    out = ARTIFACTS / f"agent_run_{int(t_start)}.json"
    out.write_text(json.dumps({"product": product, "country": country, "urls": urls, "model": MODEL, "total_s": total,
                               "usage": usage, "trace": trace, "final": final}, indent=2, ensure_ascii=False))
    print("saved", out.name)


if __name__ == "__main__":
    args = sys.argv[1:] or ["Sony WH-1000XM5", "US"]
    main(args[0], args[1] if len(args) > 1 else "US", args[2:])
