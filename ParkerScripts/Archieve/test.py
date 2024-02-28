import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def open_url_in_browser(url):
    # Configure Chrome to run in headless mode
    chrome_options = Options()
    chrome_options.headless = True
    chrome_options.add_argument("--no-sandbox")  # Recommended for headless mode
    chrome_options.add_argument("--disable-gpu")

    # Path to your ChromeDriver
    driver_path = r"C:\Python3\chromedriver.exe"

    # Ensure each thread creates its own WebDriver instance
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Open the URL
    driver.get(url)

    # Example action: Print the title of the page
    print(f"Thread: {threading.get_ident()}, URL: {url}, Title: {driver.title}")

    # Clean up: Quit the browser once done
    time.sleep(10)

    driver.quit()

# List of URLs to be opened
urls = [
    "http://example.com",
    "https://www.python.org",
    "https://selenium.dev"
]

# Creating and starting a thread for each URL
for url in urls:
    thread = threading.Thread(target=open_url_in_browser, args=(url,))
    thread.start()
