import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import re

def get_pagination_urls(start_url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = ChromeService(executable_path=r"C:\Python3\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(start_url)

    pagination_urls = []

    try:
        # Find all <a> elements
        pagination_elements = driver.find_elements(By.TAG_NAME, "a")

        for element in pagination_elements:
            try:
                text = element.text.strip()
                # Check if the text is strictly numeric
                if re.match(r'^\d+$', text):
                    url = element.get_attribute('href')
                    if url and url not in pagination_urls:
                        pagination_urls.append(url)
            except NoSuchElementException:
                continue
    except NoSuchElementException:
        pass

    driver.quit()

    return pagination_urls

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python get_pagination.py <start_url>")
        sys.exit(1)

    start_url = sys.argv[1]
    urls = get_pagination_urls(start_url)
    print(urls)
