from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# XPATHs extracted from the HTML file you provided
ROOM_ROW_XPATH = "//div[@class='rdRow']"
ROOM_NAME_XPATH = ".//div[@class='roomTypeText']"
ROOM_PRICE_XPATH = ".//div[@class='rdrLeft rdrBold']//span"


def parse_hotel_details_page(driver, hotel_name=None, hotel_url=None, stay_from=None, stay_to=None):
    """
    Extract room names and prices from hotel-details page.
    """
    rooms_data = []
    
    # Wait for the rooms to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, ROOM_ROW_XPATH))
    )
    
    rows = driver.find_elements(By.XPATH, ROOM_ROW_XPATH)
    
    for row in rows:
        try:
            # Extract room name
            name_el = row.find_element(By.XPATH, ROOM_NAME_XPATH)
            room_name = name_el.text.strip()
            
            # Extract price
            price_el = row.find_element(By.XPATH, ROOM_PRICE_XPATH)
            price_text = price_el.text.strip()
            
            # Extract currency if needed (e.g., from "SAR 143.62")
            parts = price_text.split()
            if len(parts) >= 2:
                currency = parts[0]
                price_value = parts[1]
            else:
                currency = "SAR"  # Default
                price_value = price_text
            
            rooms_data.append(
                {
                    "hotel_name": hotel_name,
                    "hotel_url": hotel_url,
                    "room_name": room_name,
                    "price": price_value,
                    "currency": currency,
                    "stay_from": stay_from,
                    "stay_to": stay_to,
                }
            )
        except Exception as e:
            print(f"Error extracting room data: {e}")
            continue
    
    return rooms_data