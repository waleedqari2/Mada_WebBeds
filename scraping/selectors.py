"""
ضع هنا كل الـ selectors (XPATH, CSS) التي ستستخدمها للحقول والأزرار.
سنملؤها عندما ترسل لي بيانات الأزرار / HTML.
"""

# أمثلة مؤقتة، استبدلها بما سترسله:
SEARCH_BUTTON_XPATH = "//button[@id='searchButton']"
DESTINATION_INPUT_XPATH = "//input[@id='destination']"
CHECKIN_INPUT_XPATH = "//input[@id='checkin']"
CHECKOUT_INPUT_XPATH = "//input[@id='checkout']"
GUESTS_INPUT_XPATH = "//input[@id='guests']"

# نتائج الفنادق (صف)
HOTEL_ROW_XPATH = "//div[@class='hotel-row']"

# اسم الفندق داخل الصف
HOTEL_NAME_XPATH = ".//span[@class='hotel-name']"

# سعر الفندق داخل الصف
HOTEL_PRICE_XPATH = ".//span[@class='hotel-price']"

# زر الصفحة التالية
NEXT_PAGE_BUTTON_XPATH = "//button[@id='nextPage']"