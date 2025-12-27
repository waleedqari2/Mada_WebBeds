from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from . import config
from . import selectors


def open_search_page(driver):
    driver.get(config.BASE_URL)


def fill_search_form(driver, destination, checkin, checkout, guests):
    wait = WebDriverWait(driver, config.EXPLICIT_WAIT)

    # مثال، استبدل بالـ selectors الحقيقية
    dest_input = wait.until(
        EC.presence_of_element_located((By.XPATH, selectors.DESTINATION_INPUT_XPATH))
    )
    dest_input.clear()
    dest_input.send_keys(destination)

    checkin_input = driver.find_element(By.XPATH, selectors.CHECKIN_INPUT_XPATH)
    checkin_input.clear()
    checkin_input.send_keys(checkin)

    checkout_input = driver.find_element(By.XPATH, selectors.CHECKOUT_INPUT_XPATH)
    checkout_input.clear()
    checkout_input.send_keys(checkout)

    guests_input = driver.find_element(By.XPATH, selectors.GUESTS_INPUT_XPATH)
    guests_input.clear()
    guests_input.send_keys(str(guests))


def click_search(driver):
    wait = WebDriverWait(driver, config.EXPLICIT_WAIT)
    search_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, selectors.SEARCH_BUTTON_XPATH))
    )
    search_button.click()


def go_to_next_page_if_exists(driver):
    """
    يحاول الانتقال للصفحة التالية، يرجع True لو انتقل، False لو لا يوجد صفحة تالية.
    """
    try:
        wait = WebDriverWait(driver, config.EXPLICIT_WAIT)
        next_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, selectors.NEXT_PAGE_BUTTON_XPATH))
        )
        next_btn.click()
        return True
    except Exception:
        return False