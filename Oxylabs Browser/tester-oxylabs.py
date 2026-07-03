import json
import random
import string
import os
from playwright.sync_api import sync_playwright

# Define params for connecting to Oxylabs servers
username = "<your-oxylabs-username>"
password = "<your-oxylabs-password>"
endpoint = "ubc.oxylabs.io"

# Create folder for screenshots
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

def get_session():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

# Define Chrome arguments
chrome_args = json.dumps([
    "--disable-blink-features=AutomationControlled", 
    "--enable-features=NetworkServiceInProcess"
])

# Define params for Oxylabs Headless Browser
params = f"p_device=mobile&p_cc=US&p_session_id={get_session()}&args={chrome_args}"
browser_url = f"wss://{username}:{password}@{endpoint}?{params}"

targets = [
    ("<https://www.empire-cat.com/equipment/used/catalog/aa/j1s03815>", "Kasada"),
    ("<https://www.ssense.com/en-us/men/designers/acne-studios>", "Cloudflare"),
    ("<https://loccitane.com/en-us/olio-jeunesse-divine-30ml-27DH030I22.html>", "DataDome"),
    ("<https://www.gucci.com/us/en/pr/women/shoes-for-women/sandals-for-women/flat-sandals-for-women/womens-slide-sandal-with-horsebit-p-834427AAE046273>", "Akamai")
]

# Define semantics to intercept in responses
BLOCK_TITLES = ["just a moment", "access denied", "attention required", "security measure", "not acceptable", "403 forbidden"]
results = []

def run_benchmark():
    with sync_playwright() as p:
        for url, antibot in targets:
            print(f"---\nTesting {antibot}...")
            try:
                browser = p.chromium.connect_over_cdp(browser_url)
                context = browser.new_context()
                page = context.new_page()

                captcha_detected = False
                def handle_log(msg):
                    nonlocal captcha_detected
                    if "oxylabs-captcha-solve-start" in msg.text:
                        print(f"   [Solver] {antibot} challenge detected...")
                        captcha_detected = True
                    elif "oxylabs-captcha-solve-end" in msg.text:
                        print(f"   [Solver] {antibot} resolved!")
                        captcha_detected = False

                page.on("console", handle_log)
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
                
                # Wait for the page to stabilize
                if captcha_detected:
                    page.wait_for_timeout(15000)
                else:
                    page.wait_for_timeout(8000)

                # Make and save screenshots
                screenshot_path = f"screenshots/{antibot.lower()}_result.png"
                page.screenshot(path=screenshot_path, full_page=False)
                print(f"   [Camera] Screenshot saved: {screenshot_path}")

                title = page.title() or ""
                low_title = title.lower()
                is_blocked = any(bt in low_title for bt in BLOCK_TITLES)
                
                if len(title) > 5 and not is_blocked:
                    print(f"✅ {antibot} PASS: {title[:30]}...")
                    results.append({"url": url, "antibot": antibot, "status": "ok", "title": title})
                else:
                    print(f"❌ {antibot} FAIL: {title}")
                    results.append({"url": url, "antibot": antibot, "status": "fail", "error": title})

                browser.close()

            except Exception as e:
                print(f"❌ {antibot} Exception: {str(e)[:50]}")

run_benchmark()