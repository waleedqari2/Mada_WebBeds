from datetime import datetime, timedelta
from typing import List, Dict
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from .selenium_client import create_driver, load_cookies
from . import parsers


DATE_FMT_UI = "%d/%m/%Y"   # 27/03/2026
DATE_FMT_URL = "%Y-%m-%d"  # 2026-03-27


def generate_night_ranges(date_from_str: str, date_to_str: str) -> List[Dict]:
    """
    Split the period into individual nights.
    E.g., from 01/02/2026 to 05/02/2026 =>
      01→02, 02→03, 03→04, 04→05
    """
    d_from = datetime.strptime(date_from_str, DATE_FMT_UI)
    d_to = datetime.strptime(date_to_str, DATE_FMT_UI)

    ranges = []
    cur = d_from
    while cur < d_to:
        nxt = cur + timedelta(days=1)
        if nxt > d_to:
            break
        ranges.append(
            {
                "from": cur.strftime(DATE_FMT_UI),
                "to": nxt.strftime(DATE_FMT_UI),
                "from_iso": cur.strftime(DATE_FMT_URL),
                "to_iso": nxt.strftime(DATE_FMT_URL),
            }
        )
        cur = nxt
    return ranges


def modify_url_with_dates(base_url: str, from_iso: str, to_iso: str) -> str:
    """
    Modify the URL parameters for DateFrom, dateFrom, DateTo, dateTo, and numberOfNights.
    """
    parsed_url = urlparse(base_url)
    query_params = parse_qs(parsed_url.query)
    
    # Update dates
    query_params['DateFrom'] = [from_iso.replace('-', '/').replace('/', '%2F')]
    query_params['dateFrom'] = [from_iso]
    query_params['DateTo'] = [to_iso.replace('-', '/').replace('/', '%2F')]
    query_params['dateTo'] = [to_iso]
    query_params['numberOfNights'] = ['1']  # Assuming 1 night per search
    
    # Rebuild URL
    new_query = urlencode(query_params, doseq=True)
    new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, new_query, parsed_url.fragment))
    return new_url


def scrape_full_stay_for_hotels(hotels: Dict[str, str]) -> list:
    """
    Scrape for full stay period using the base URLs.
    """
    driver = create_driver()
    load_cookies(driver)

    all_rows = []
    try:
        for hotel_name, url in hotels.items():
            print(f"🔎 Opening hotel URL: {url}")
            driver.get(url)
            rooms = parsers.parse_hotel_details_page(driver, hotel_name=hotel_name, hotel_url=url)
            print(f"➡ Extracted {len(rooms)} rooms from {hotel_name}.")
            all_rows.extend(rooms)
        return all_rows
    finally:
        driver.quit()


def scrape_night_by_night_for_hotels(hotels: Dict[str, str], night_ranges: List[Dict]) -> list:
    """
    Scrape night by night by modifying URLs for each night range.
    """
    driver = create_driver()
    load_cookies(driver)

    all_rows = []
    try:
        for hotel_name, base_url in hotels.items():
            for nr in night_ranges:
                modified_url = modify_url_with_dates(base_url, nr["from_iso"], nr["to_iso"])
                print(f"🔎 Opening modified URL for {hotel_name}: {modified_url}")
                driver.get(modified_url)
                rooms = parsers.parse_hotel_details_page(
                    driver,
                    hotel_name=hotel_name,
                    hotel_url=modified_url,
                    stay_from=nr["from"],
                    stay_to=nr["to"],
                )
                print(f"➡ Extracted {len(rooms)} rooms for {nr['from']} → {nr['to']} from {hotel_name}.")
                all_rows.extend(rooms)
        return all_rows
    finally:
        driver.quit()