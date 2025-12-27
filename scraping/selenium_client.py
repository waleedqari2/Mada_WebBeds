# Simple selenium helper: create_driver() and load_cookies()
# Place this file under scraping/ to match imports in the rest of the project.

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import json

load_dotenv()  # load .env if present

def create_driver():
    """
    Create and return a Selenium Chrome WebDriver.
    Uses CHROMEDRIVER_PATH if set, otherwise webdriver-manager to install driver.
    Honors HEADLESS env var.
    """
    chrome_opts = Options()
    headless = os.getenv("HEADLESS", "true").lower() in ("1", "true", "yes")
    if headless:
        chrome_opts.add_argument("--headless=new")
    chrome_opts.add_argument("--no-sandbox")
    chrome_opts.add_argument("--disable-dev-shm-usage")
    chrome_opts.add_argument("--disable-gpu")
    chrome_opts.add_argument("--window-size=1920,1080")
    chrome_opts.add_argument("--ignore-certificate-errors")
    chrome_opts.add_argument("--disable-extensions")
    chrome_opts.add_argument("--disable-blink-features=AutomationControlled")

    chromedriver_path = os.getenv("CHROMEDRIVER_PATH", "").strip()

    if chromedriver_path:
        service = ChromeService(executable_path=chromedriver_path)
    else:
        # use webdriver-manager to download appropriate chromedriver
        service = ChromeService(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=chrome_opts)
    # small implicit wait, rely mainly on explicit waits
    driver.implicitly_wait(2)
    return driver

def load_cookies(driver, cookie_file=None, base_url="https://www.dotwconnect.com"):
    """
    Load cookies from a JSON file into the given driver.
    cookie_file: path to cookies.json (format produced by browser extension or custom exporter).
    base_url: driver must be on same domain before adding cookies.
    """
    cookie_file = cookie_file or os.getenv("COOKIE_FILE", "./cookies.json")
    if not os.path.exists(cookie_file):
        print(f"[cookies] file not found: {cookie_file}")
        return False

    # Load a base page to set domain
    driver.get(base_url)
    time.sleep(1)

    try:
        with open(cookie_file, "r", encoding="utf-8") as fh:
            cookies = json.load(fh)
    except Exception as e:
        print(f"[cookies] error reading {cookie_file}: {e}")
        return False

    added = 0
    for c in cookies:
        # Normalize cookie dict keys if necessary
        cookie = {
            "name": c.get("name") or c.get("Name"),
            "value": c.get("value") or c.get("Value"),
            "domain": c.get("domain") or c.get("Domain", None),
            "path": c.get("path", "/"),
            "expiry": c.get("expiry") or c.get("expirationDate") or c.get("Expires"),
            "httpOnly": c.get("httpOnly", False),
            "secure": c.get("secure", False),
        }
        # Selenium requires domain omitted/valid; try to add cookie
        try:
            # remove None values that Selenium might not like
            cookie_clean = {k: v for k, v in cookie.items() if v is not None}
            driver.add_cookie(cookie_clean)
            added += 1
        except Exception as e:
            # some cookies (e.g., starting with __Host-) may require adjustments; skip on error
            # print(f"[cookies] skip cookie {cookie.get('name')}: {e}")
            continue

    print(f"[cookies] loaded {added} cookies from {cookie_file}")
    return True