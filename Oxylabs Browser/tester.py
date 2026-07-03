from playwright.sync_api import sync_playwright

# Target pages with their anti-bots
targets = [
    ("<https://www.ssense.com/en-us/men/designers/acne-studios>", "Cloudflare"),
    ("<https://www.gucci.com/us/en/pr/women/shoes-for-women/sandals-for-women/flat-sandals-for-women/womens-slide-sandal-with-horsebit-p-834427AAE046273>", "Akamai"),
    ("<https://loccitane.com/en-us/olio-jeunesse-divine-30ml-27DH030I22.html>", "DataDome"),
    ("<https://www.empire-cat.com/equipment/used/catalog/aa/j1s03815>", "Kasada")
]

results = []

# List of titles or substrings that indicate common blocks/challenges
BLOCK_INDICATORS = [
    "just a moment", "access denied", "attention required", 
    "cloudflare", "ddos protection", "captcha", "verify you are human"
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()

    for url, antibot in targets:
        page = context.new_page()
        try:
            # We capture the response to check the status code
            response = page.goto(url, wait_until="domcontentloaded")
            page.wait_for_timeout(5000)

            title = page.title() or ""
            status_code = response.status if response else 0
            
            # Validation Logic
            is_blocked = False
            error_reason = ""

            # 1. Check HTTP Status (403 Forbidden is a classic block)
            if status_code >= 400:
                is_blocked = True
                error_reason = f"HTTP {status_code}"
            
            # 2. Check for "Waiting Room" or "Block Page" titles
            elif any(indicator in title.lower() for indicator in BLOCK_INDICATORS):
                is_blocked = True
                error_reason = "Challenge/Block Page detected"
            
            # 3. Check for empty titles (Common with Kasada/DataDome blocks)
            elif not title or title.strip() == "":
                is_blocked = True
                error_reason = "Empty/N/A Title (Hidden Block)"

            if is_blocked:
                results.append({"url": url, "antibot": antibot, "title": title, "status": "fail", "error": error_reason})
                print(f"❌ [{antibot}] Blocked: {error_reason}")
            else:
                results.append({"url": url, "antibot": antibot, "title": title, "status": "ok"})
                print(f"✅ [{antibot}] Success: {title}")

        except Exception as e:
            error_msg = str(e).split('\n')[0] # Keep it brief
            print(f"❌ [{antibot}] Exception: {error_msg}")
            results.append({"url": url, "antibot": antibot, "title": None, "status": "fail", "error": error_msg})

        finally:
            page.close()

    browser.close()

# Print summary table
passed = sum(1 for r in results if r.get("status") == "ok")
failed = len(results) - passed

print("\n" + "=" * 105)
print(f"{'STATUS':<10} {'ANTIBOT':<12} {'RESULT/REASON':<30} {'URL'}")
print("=" * 105)
for r in results:
    status = "✅ PASS" if r.get("status") == "ok" else "❌ FAIL"
    antibot = r.get("antibot", "N/A")
    # Show the reason if it failed, otherwise show the page title
    display_info = r.get("error") if r.get("status") == "fail" else r.get("title", "N/A")
    print(f"{status:<10} {antibot:<12} {str(display_info)[:28]:<30} {r['url']}")
print("=" * 105)
print(f"✅ Passes: {passed}  |  ❌ Fails: {failed}  |  Total: {len(results)}")
print("=" * 105)