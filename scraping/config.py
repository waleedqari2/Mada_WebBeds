import os

CHROMEDRIVER_PATH = r"C:\Users\PC001\Desktop\webbesa\chromedriver.exe"
BASE_URL = "https://www.dotwconnect.com/interface/en/login"

BASE_DIR = os.path.dirname(__file__)
COOKIES_FILE = os.path.join(BASE_DIR, "cookies.json")

OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)