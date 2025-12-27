import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from . import config
from . import parsers
from . import storage
from .hotels_list import HOTEL_URLS


def load_cookies_if_exist(driver):
    try:
        with open(config.COOKIES_FILE, "r", encoding="utf-8") as f:
            cookies = json.load(f)
    except FileNotFoundError:
        print("⚠️ ملف الكوكيز غير موجود، سيتم التصفح بدون كوكيز.")
        return

    driver.get(config.BASE_URL)
    time.sleep(2)

    for cookie in cookies:
        if cookie.get("sameSite") is None:
            cookie.pop("sameSite", None)

        cookie_dict = {
            "name": cookie.get("name"),
            "value": cookie.get("value"),
            "domain": cookie.get("domain"),
            "path": cookie.get("path", "/"),
            "secure": cookie.get("secure", False),
            "httpOnly": cookie.get("httpOnly", False),
        }

        exp = cookie.get("expirationDate")
        if exp:
            cookie_dict["expiry"] = int(exp)

        try:
            driver.add_cookie(cookie_dict)
        except Exception:
            continue

    driver.refresh()
    time.sleep(3)


def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    service = Service(config.CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(config.IMPLICIT_WAIT)
    return driver


def scrape_multiple_hotels():
    driver = create_driver()
    try:
        load_cookies_if_exist(driver)

        all_rooms = []

        for url in HOTEL_URLS:
            print(f"🔎 فتح رابط الفندق: {url}")
            driver.get(url)
            time.sleep(5)  # انتظر تحميل الصفحة

            rooms = parsers.parse_hotel_details_page(driver, hotel_url=url)
            print(f"➡ تم استخراج {len(rooms)} غرفة من هذا الفندق.")
            all_rooms.extend(rooms)

        storage.save_to_csv(all_rooms)
        storage.save_to_json(all_rooms)

        print(f"✅ تم استخراج إجمالي {len(all_rooms)} غرفة/سعر من كل الفنادق.")
        print(f"📄 CSV: {config.OUTPUT_CSV}")
        print(f"📄 JSON: {config.OUTPUT_JSON}")
    finally:
        # علّق هذا لو حابب تراجع الصفحات في المتصفح بعد التشغيل
        # driver.quit()
        pass


if __name__ == "__main__":
    scrape_multiple_hotels()